/*
 * Copyright (C) 2017 - 2022, Stephan Mueller <smueller@chronox.de>
 *
 * License: see LICENSE file
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 */

#include <string.h>
#include <sys/types.h>

#include "parser.h"
#include "stringhelper.h"
#include "read_json.h"
#include "logger.h"

#include "parser_common.h"
#include "parser_sym.h"

static struct sym_backend *sym_backend = NULL;

static void sym_mct_cfb8_enqueue(struct buffer *dst, uint8_t val)
{
	size_t a;

	/*
	 * memmove by one byte (oldest byte is left-most to reuse buffer for
	 * key update)
	 */
	for (a = 0; a < dst->len - 1; a++)
		dst->buf[a] = dst->buf[a + 1];

	/* add ciphertext byte */
	dst->buf[dst->len - 1] = val;
}

static void sym_mct_cfb1_enqueue(struct buffer *dst, uint8_t val)
{
	ssize_t a;
	uint8_t msb_prev = 0;

	/*
	 * bit-memmove by one bit (oldest bit is
	 * left-most to reuse buffer for key update)
	 */
	for (a = (ssize_t)(dst->len - 1); a >= 0; a--) {
		/* remember MSB of current byte */
		uint8_t tmp = dst->buf[a]>>7;

		/* roll byte by one */
		dst->buf[a] = (unsigned char)(dst->buf[a]<<1);
		/* add the MSB of previous byte as LSB for this byte */
		dst->buf[a] |= msb_prev;
		msb_prev = tmp;
	}

	/* add ciphertext bit */
	dst->buf[dst->len - 1] |= val>>7;
}

/*
 * DES keys uses only the 7 high bits of a byte, the 8th low bit
 * is the parity bit
 * as the new key is calculated from oldkey XOR cipher in the MCT test,
 * the parity is not really checked and needs to be set to match
 * expectation (OpenSSL does not really care, but the FIPS
 * test result is expected that the key has the appropriate parity)
 * $1: arbitrary binary string
 * returns: string with odd parity set in low bit of each byte
 */
/* implied in this function: key must be at least 8 bytes */
static void tdes_fix_parity(unsigned char *key)
{
	unsigned int i = 0;

	for (i = 0; i < 8; i++) {
		unsigned char byte = key[i];
		unsigned int j = 0;
		unsigned int odd = 0;

		for (j = 0; j < 8; j++) {
			if (byte & (1<<j))
				odd++;
		}

		/* check if parity is already odd */
		if (!(odd & 1))
			key[i] ^= 1; /* set the low bit */
	}
}

#define max(x, y)	((x < y) ? y : x)

/*
 * Who invented that test was on crack - perhaps I should have gotten also some
 * weed before reading the test definition.
 *
 * PS: This code is pure spaghetti code - but I do not care as TDES
 * will be sunset in the not too distant future anyways. Do not bother to send
 * patches for it. It works even when it is a nightmare of code.
 */
static int sym_mct_tdes_helper(const struct json_array *processdata,
			       flags_t parsed_flags,
			       struct json_object *testvector,
			       struct json_object *testresults,
			       int (*callback)(struct sym_data *vector,
					       flags_t parsed_flags),
			       struct sym_data *vector)
{
	unsigned int oloop = 0;
	unsigned int iloop = 0;
	int ret = 1;
	BUFFER_INIT(calc_data);
	BUFFER_INIT(old_calc_data);
	BUFFER_INIT(old_old_calc_data);
	BUFFER_INIT(cfb_calc_data);
	BUFFER_INIT(cfb_old_calc_data);
	BUFFER_INIT(inittext);
	BUFFER_INIT(last_iv);
	BUFFER_INIT(otmp);
	BUFFER_INIT(tmp2);
	struct json_object *testresult, *resultsarray;

	(void)testvector;
	(void)callback;

	if (!sym_backend->mct_init ||
	    !sym_backend->mct_update ||
	    !sym_backend->mct_fini)
		return -EOPNOTSUPP;

	CKINT(alloc_buf(vector->key.len + vector->key2.len + vector->key3.len,
			&otmp));
	memcpy(otmp.buf, vector->key.buf, vector->key.len);
	memcpy(otmp.buf + vector->key.len, vector->key2.buf, vector->key2.len);
	memcpy(otmp.buf + vector->key.len + vector->key2.len, vector->key3.buf,
	       vector->key3.len);

	/* save original key pointer */
	copy_ptr_buf(&tmp2, &vector->key);
	/* move new key pointer into vector->key */
	copy_ptr_buf(&vector->key, &otmp);

	if (vector->cipher != ACVP_TDESCFB1 &&
	    vector->cipher != ACVP_TDESCFB8 &&
	    vector->data.len != vector->key.len / 3) {
		logger(LOGGER_VERBOSE,
		       "Mismatch in key length and data block length\n");
		return -EINVAL;
	}

	/*
	 * Create output stream.
	 */
	resultsarray = json_object_new_array();
	CKNULL(resultsarray, -ENOMEM);
	testresult = json_object_new_object();
	CKNULL(testresult, -ENOMEM);
	CKINT(json_add_test_data(testvector, testresult));

	if (vector->cipher == ACVP_TDESCFB1 ||
	    vector->cipher == ACVP_TDESCFB8) {
		if (vector->iv.len > vector->key.len) {
			logger(LOGGER_WARN,
			       "IV buffer length larger than key length!\n");
			return -EINVAL;
		}
		CKINT(alloc_buf(vector->key.len, &calc_data));
		CKINT(alloc_buf(vector->key.len, &old_calc_data));
	} else {
		CKINT(alloc_buf(vector->data.len, &calc_data));
		CKINT(alloc_buf(vector->data.len, &old_calc_data));
	}
	CKINT(alloc_buf(vector->data.len, &cfb_calc_data));
	CKINT(alloc_buf(vector->data.len, &cfb_old_calc_data));
	CKINT(alloc_buf(vector->data.len, &old_old_calc_data));
	CKINT(alloc_buf(vector->data.len, &inittext));
	CKINT(alloc_buf(vector->iv.len, &last_iv));

	for (oloop = 0; oloop < 400; oloop++) {
		BUFFER_INIT(keybuf);
		size_t i, k;
		struct json_object *single_mct_result;
		const struct json_entry *entry;
		uint8_t cfb_byte_for_next_round = 0;

		if (vector->cipher != ACVP_TDESECB)
			/* right-pad in case of CFB 1/8 */
			memcpy(calc_data.buf + calc_data.len - vector->iv.len,
			       vector->iv.buf, vector->iv.len);

		CKINT(sym_backend->mct_init(vector, parsed_flags));

		memcpy(inittext.buf, vector->data.buf, vector->data.len);

		/*
		 * Create the output JSON stream holding the test
		 * results.
		 */
		single_mct_result = json_object_new_object();
		CKNULL(single_mct_result, ENOMEM);

		keybuf.len = vector->key2.len;
		keybuf.buf = vector->key.buf;
		CKINT(json_add_bin2hex(single_mct_result, "key1", &keybuf));

		keybuf.buf = vector->key.buf + vector->key2.len;
		CKINT(json_add_bin2hex(single_mct_result, "key2", &keybuf));

		keybuf.buf = vector->key.buf + (2 * vector->key2.len);
		CKINT(json_add_bin2hex(single_mct_result, "key3", &keybuf));
		CKINT(json_add_bin2hex(single_mct_result,
				       (parsed_flags & FLAG_OP_ENC) ?
				        "pt" : "ct", &vector->data));

		for (iloop = 0; iloop < 9999; iloop++) {
			struct buffer itmp;

			memcpy(old_old_calc_data.buf, old_calc_data.buf,
			       vector->data.len);
			/* we need that for key calculation */
			memcpy(old_calc_data.buf + old_calc_data.len - vector->data.len,
			       vector->data.buf, vector->data.len);

			if (vector->cipher == ACVP_TDESOFB) {
				memcpy(cfb_old_calc_data.buf, vector->data.buf,
				       vector->data.len);
 			}

			CKINT(sym_backend->mct_update(vector, parsed_flags));

			if (((parsed_flags & FLAG_OP_ENC) &&
			     (vector->cipher == ACVP_TDESCBC ||
			      vector->cipher == ACVP_TDESCFB64)) ||
			      vector->cipher == ACVP_TDESOFB) {
				memcpy(old_calc_data.buf, vector->data.buf,
				       vector->data.len);

				/* Ciphertext is the new plaintext */
				copy_ptr_buf(&itmp, &vector->data);
				copy_ptr_buf(&vector->data, &calc_data);
				copy_ptr_buf(&calc_data, &itmp);
			}

			/* Next input is the previous IV */
			if (vector->cipher == ACVP_TDESOFB) {
				unsigned int idx;

				for (idx = 0; idx < vector->data.len; idx++) {
					calc_data.buf[idx] ^=
						cfb_old_calc_data.buf[idx];
				}
			}

			if (!(parsed_flags & FLAG_OP_ENC) &&
			    vector->cipher == ACVP_TDESCFB64) {
				unsigned int a;

				memcpy(cfb_old_calc_data.buf, cfb_calc_data.buf,
				       calc_data.len);
				memcpy(cfb_calc_data.buf, vector->data.buf,
				       vector->data.len);
				for (a = 0; a < vector->data.len; a++)
					vector->data.buf[a] ^=
						old_calc_data.buf[a];
			}

			if (vector->cipher == ACVP_TDESCFB8) {
				if (parsed_flags & FLAG_OP_ENC) {
					uint8_t tmp =
						calc_data.buf[calc_data.len - 8];

					sym_mct_cfb8_enqueue(&calc_data,
							vector->data.buf[0]);
					vector->data.buf[0] = tmp;
				} else {
					sym_mct_cfb8_enqueue(&calc_data,
							vector->data.buf[0]);
					vector->data.buf[0] ^=
							old_calc_data.buf[23];
					sym_mct_cfb8_enqueue(&last_iv,
							vector->data.buf[0]);
				}
			}

			if (vector->cipher == ACVP_TDESCFB1) {
				if (parsed_flags & FLAG_OP_ENC) {
					uint8_t tmp =
						calc_data.buf[calc_data.len - 8] & 1<<7;

					sym_mct_cfb1_enqueue(&calc_data,
							vector->data.buf[0]);

					vector->data.buf[0] = tmp;
				} else {
					sym_mct_cfb1_enqueue(&calc_data,
							vector->data.buf[0]);
					vector->data.buf[0] ^=  (old_calc_data.buf[23] & (1<<7));
					sym_mct_cfb1_enqueue(&last_iv,
							vector->data.buf[0]);
				}

			}
		}

		if (vector->cipher == ACVP_TDESOFB)
			memcpy(last_iv.buf, calc_data.buf, calc_data.len);

		/* we need that for key calculation */
		if (vector->cipher != ACVP_TDESCFB1)
			memcpy(calc_data.buf, vector->data.buf, vector->data.len);

		if (vector->cipher == ACVP_TDESCFB64) {
			struct buffer *i1 = (parsed_flags & FLAG_OP_ENC) ?
					     &old_old_calc_data :
					     &cfb_old_calc_data;
			struct buffer *i2 = (parsed_flags & FLAG_OP_ENC) ?
					     &old_calc_data :
					     &cfb_calc_data;
			unsigned int idx;

			for (idx = 0; idx < vector->iv.len; idx++) {
				last_iv.buf[idx] = i1->buf[idx] ^ i2->buf[idx];
 			}
		}

		if (vector->cipher == ACVP_TDESCFB1 &&
		    (parsed_flags & FLAG_OP_DEC)) {
			cfb_byte_for_next_round = vector->data.buf[0];
		}

		/* final invocation without shuffling */
		CKINT(sym_backend->mct_update(vector, parsed_flags));

		/* Enqueue generated byte into calc_data */
		if (vector->cipher == ACVP_TDESCFB8) {
			if (parsed_flags & FLAG_OP_ENC) {
				cfb_byte_for_next_round =
					calc_data.buf[calc_data.len - 8];
				sym_mct_cfb8_enqueue(&calc_data,
						     vector->data.buf[0]);
			} else {
				cfb_byte_for_next_round = vector->data.buf[0] ^
							calc_data.buf[0];
				sym_mct_cfb8_enqueue(&calc_data,
						     vector->data.buf[0]);
			}
		}

		/* Enqueue generated bit into calc_data */
		if (vector->cipher == ACVP_TDESCFB1) {
			if (parsed_flags & FLAG_OP_ENC) {
				cfb_byte_for_next_round =
					calc_data.buf[calc_data.len - 8] & 1<<7;
				sym_mct_cfb1_enqueue(&calc_data,
						     vector->data.buf[0]);
			} else {
				cfb_byte_for_next_round ^= vector->data.buf[0];
				sym_mct_cfb1_enqueue(&calc_data,
						     vector->data.buf[0]);
			}
		}

		if (vector->cipher == ACVP_TDESCFB8 ||
		    vector->cipher == ACVP_TDESCFB1) {
			if (parsed_flags & FLAG_OP_ENC)
				memcpy(last_iv.buf,
				       calc_data.buf + calc_data.len -
								last_iv.len,
				       last_iv.len);
			/* Decryption last IV is generated in the loop above */
		}

		CKINT(sym_backend->mct_fini(vector, parsed_flags));

		/* Iterate over each write definition and invoke it. */
		for_each_testresult(processdata->testresult, entry, i)
			CKINT(write_one_entry(entry, single_mct_result,
					      parsed_flags));

		if (vector->cipher == ACVP_TDESOFB) {
			unsigned int idx;

			for (idx = 0; idx < vector->iv.len; idx++) {
				vector->iv.buf[idx] = vector->data.buf[idx] ^
						      calc_data.buf[idx];
			}
		}

		if (vector->cipher == ACVP_TDESCFB64) {
			if (parsed_flags & FLAG_OP_ENC)
				memcpy(vector->iv.buf, vector->data.buf,
				       vector->iv.len);
			else
				memcpy(vector->iv.buf, calc_data.buf,
				       calc_data.len);
		}

		/* Append the output JSON stream with test results. */
		json_object_array_add(resultsarray, single_mct_result);

		/* Set K2 and handle K1 == K2 or K1 != K2 */
		if (!memcmp(vector->key.buf, vector->key.buf + 8, 8)) {
			for (i = 0; i < vector->data.len; i++)
				vector->key.buf[(i + vector->data.len)] ^=
					vector->data.buf[i];
		} else {
			if (vector->cipher == ACVP_TDESCFB8 ||
			    vector->cipher == ACVP_TDESCFB1) {
				for (k = 8; k < 16; k++)
					vector->key.buf[k] ^= calc_data.buf[k];

				/* Use the rightmost 8 bytes as new IV */
				if (parsed_flags & FLAG_OP_ENC)
					memcpy(vector->iv.buf,
					       calc_data.buf + calc_data.len - vector->iv.len,
					       vector->iv.len);
				else
					memcpy(vector->iv.buf,
					       last_iv.buf,
					       vector->iv.len);

				vector->data.buf[0] = cfb_byte_for_next_round;
			} else if (!(parsed_flags & FLAG_OP_ENC) &&
			    (vector->cipher == ACVP_TDESCFB64)) {
				for (i = 0; i < old_calc_data.len; i++)
					vector->key.buf[(i + (vector->data.len))] ^= cfb_calc_data.buf[i];
			} else if (((parsed_flags & FLAG_OP_ENC) &&
				    (vector->cipher == ACVP_TDESCBC ||
				     vector->cipher == ACVP_TDESCFB64)) ||
				     vector->cipher == ACVP_TDESOFB) {
				for (i = 0; i < old_calc_data.len; i++)
					vector->key.buf[(i + 8)] ^= old_calc_data.buf[i];
			} else {
				for (i = 0; i < calc_data.len; i++)
					vector->key.buf[(i + 8)] ^= calc_data.buf[i];
			}
		}
		tdes_fix_parity(vector->key.buf + 8);

		/* Set K3 and handle K1 == K3 or K1 != K3 */
		if (!memcmp(vector->key.buf, vector->key.buf + (8 * 2), 8)) {
			if (vector->cipher == ACVP_TDESCFB8 ||
			    vector->cipher == ACVP_TDESCFB1) {
				for (k = 0; k < 8; k++)
					vector->key.buf[(k + (8 * 2))] ^=
						calc_data.buf[k + 16];
			} else {
				for (i = 0, k = 0;
				     i < vector->data.len && k < vector->key.len - (2*8);
				     i++, k++)
					vector->key.buf[(k + (8 * 2))] ^=
						vector->data.buf[i];
			}
		} else {
			if (!(parsed_flags & FLAG_OP_ENC) &&
			     (vector->cipher == ACVP_TDESCFB64)) {
				for (i = 0; i < vector->data.len; i++)
					vector->key.buf[(i + (vector->data.len * 2))] ^= cfb_old_calc_data.buf[i];
			} else if (vector->cipher == ACVP_TDESOFB) {
				for (i = 0, k = 0;
				     i < old_old_calc_data.len &&
				      k < vector->key.len - (2*8);
				     i++)
					vector->key.buf[(i + (vector->data.len * 2))] ^= old_old_calc_data.buf[i];
			} else if ((parsed_flags & FLAG_OP_ENC) &&
				   (vector->cipher == ACVP_TDESCBC ||
				    (vector->cipher == ACVP_TDESCFB64))) {
				for (i = 0, k = 0;
				     i < calc_data.len &&
				      k < vector->key.len - (2*8);
				     i++, k++)
					vector->key.buf[(i + (8 * 2))] ^= calc_data.buf[i];
			} else if (vector->cipher == ACVP_TDESCFB8 ||
				   vector->cipher == ACVP_TDESCFB1) {
				for (k = 16; k < 24; k++)
					vector->key.buf[k] ^= calc_data.buf[k - 16];
			} else {
				for (i = 0, k = 0;
				     i < old_calc_data.len &&
				      k < vector->key.len - (2*8);
				     i++, k++)
					vector->key.buf[(i + (8 * 2))] ^= old_calc_data.buf[i];
			}

		}
		tdes_fix_parity(vector->key.buf + (8 * 2));

		/* Set K1 */
		if (vector->cipher == ACVP_TDESCFB8 ||
		    vector->cipher == ACVP_TDESCFB1) {
			for (k = 0; k < 8; k++)
				vector->key.buf[k] ^= calc_data.buf[k + 16];
		} else {
			for (i = 0; i < vector->data.len; i++)
				vector->key.buf[i] ^= vector->data.buf[i];
		}
		tdes_fix_parity(vector->key.buf);

		if (vector->cipher == ACVP_TDESCBC) {
			if (parsed_flags & FLAG_OP_ENC) {
				memcpy(vector->iv.buf, vector->data.buf,
				       vector->iv.len);
				memcpy(vector->data.buf, old_calc_data.buf,
				       vector->data.len);

			} else
				memcpy(vector->iv.buf, calc_data.buf,
				       vector->iv.len);
		}
		if (vector->cipher == ACVP_TDESCFB64) {
			if (parsed_flags & FLAG_OP_ENC) {
				memcpy(vector->data.buf, old_calc_data.buf,
				       vector->data.len);
			} else {
				unsigned int a;

				for (a = 0; a < vector->data.len; a++)
					vector->data.buf[a] ^=
						calc_data.buf[a];
			}
		}

		if (vector->cipher == ACVP_TDESOFB) {
			unsigned int a;

			for (a = 0; a < vector->data.len; a++)
				vector->data.buf[a] = inittext.buf[a] ^ last_iv.buf[a];
		}
	}

	json_object_object_add(testresult, "resultsArray", resultsarray);
	/* Append the output JSON stream with test results. */
	json_object_array_add(testresults, testresult);

	/* We have written data, generic parser should not write it. */
	ret = FLAG_RES_DATA_WRITTEN;

out:
	/* restore original key pointer */
	copy_ptr_buf(&vector->key, &tmp2);
	free_buf(&otmp);

	free_buf(&calc_data);
	free_buf(&old_calc_data);
	free_buf(&old_old_calc_data);
	free_buf(&cfb_calc_data);
	free_buf(&cfb_old_calc_data);
	free_buf(&last_iv);
	free_buf(&inittext);
	return ret;
}

static int sym_mct_aes_helper(const struct json_array *processdata,
			      flags_t parsed_flags,
			      struct json_object *testvector,
			      struct json_object *testresults,
			      int (*callback)(struct sym_data *vector,
					      flags_t parsed_flags),
			      struct sym_data *vector)
{
	uint32_t oloop = 0;
	uint32_t iloop = 0;
	int ret = -EINVAL;
	BUFFER_INIT(calc_data);
	struct json_object *testresult, *resultsarray = NULL;

	(void)callback;

	if (!sym_backend->mct_update || !sym_backend->mct_fini)
		return -EOPNOTSUPP;

	if (vector->cipher == ACVP_CFB8 || vector->cipher == ACVP_CFB1) {
		if (vector->iv.len > vector->key.len) {
			logger(LOGGER_WARN,
			       "IV buffer length larger than key length!\n");
			return -EINVAL;
		}
		CKINT(alloc_buf(vector->key.len, &calc_data));
	} else {
		CKINT(alloc_buf(vector->data.len, &calc_data));
	}

	/* Create output stream. */
	resultsarray = json_object_new_array();
	CKNULL(resultsarray, -ENOMEM);
	testresult = json_object_new_object();
	CKNULL(testresult, -ENOMEM);
	CKINT(json_add_test_data(testvector, testresult));

	for (oloop = 0; oloop < 100; oloop++) {
		size_t i, k;
		struct json_object *single_mct_result;
		const struct json_entry *entry;
		uint8_t cfb_byte_for_next_round = 0;

		if (vector->cipher != ACVP_ECB) {
			/* Only for CFB1/8 the calc_data is longer than IV */
 			memcpy(calc_data.buf + calc_data.len - vector->iv.len,
 			       vector->iv.buf, vector->iv.len);
		}

		CKNULL(sym_backend->mct_init, -EFAULT);
		CKINT(sym_backend->mct_init(vector, parsed_flags));

		/*
		 * Create the output JSON stream holding the test
		 * results.
		 */
		single_mct_result = json_object_new_object();
		CKNULL(single_mct_result, ENOMEM);

		CKINT(json_add_bin2hex(single_mct_result, "key", &vector->key));
		CKINT(json_add_bin2hex(single_mct_result,
				       (parsed_flags & FLAG_OP_ENC) ?
				        "pt" : "ct", &vector->data));

		free_buf(&vector->inner_loop_final_cj1);

		for (iloop = 0; iloop < 999; iloop++) {
			struct buffer tmp;

			logger_binary(LOGGER_DEBUG, vector->data.buf,
				      vector->data.len, "MCT source data");
			CKINT(sym_backend->mct_update(vector, parsed_flags));

			/* backend implemented inner loop */
			if (vector->inner_loop_final_cj1.len)
				break;

			logger_binary(LOGGER_DEBUG, vector->data.buf,
				      vector->data.len, "MCT calculated data");

			/* IV[i] || MSB(CT) for PT[j+1] */
			if (vector->cipher == ACVP_CBC_CS1 ||
			    vector->cipher == ACVP_CBC_CS2 ||
			    vector->cipher == ACVP_CBC_CS3) {
				if (iloop == 0) {
					memcpy(calc_data.buf, vector->iv.buf,
					       vector->iv.len);
					memcpy(calc_data.buf + vector->iv.len,
					       vector->data.buf,
					       calc_data.len - vector->iv.len);
				}
			}

			if (vector->cipher == ACVP_CFB8) {
				uint8_t ctmp = calc_data.buf[calc_data.len - 16];

				sym_mct_cfb8_enqueue(&calc_data,
						     vector->data.buf[0]);

				vector->data.buf[0] = ctmp;
			} else if (vector->cipher == ACVP_CFB1) {
				uint8_t ctmp =
					calc_data.buf[calc_data.len - 16] & 1<<7;

				sym_mct_cfb1_enqueue(&calc_data,
						     vector->data.buf[0]);

				vector->data.buf[0] = ctmp;
			} else if (vector->cipher != ACVP_ECB) {
				copy_ptr_buf(&tmp, &vector->data);
				copy_ptr_buf(&vector->data, &calc_data);
				copy_ptr_buf(&calc_data, &tmp);
			}
		}

		/* final invocation without subsequent shuffling */
		if (vector->inner_loop_final_cj1.len) {
			if (calc_data.len != vector->inner_loop_final_cj1.len) {
				logger(LOGGER_ERR,
				       "backend inner loop C[j-1] length unexpected\n");
				ret = -EINVAL;
				goto out;
			}
			memcpy(calc_data.buf, vector->inner_loop_final_cj1.buf,
			       calc_data.len);
		} else {
			/* we need that for key calculation */
			if (vector->cipher == ACVP_ECB)
				memcpy(calc_data.buf, vector->data.buf,
				       vector->data.len);
			CKINT(sym_backend->mct_update(vector, parsed_flags));

			/* Enqueue generated byte into calc_data */
			if (vector->cipher == ACVP_CFB8) {
				cfb_byte_for_next_round =
					calc_data.buf[calc_data.len - 16];
				sym_mct_cfb8_enqueue(&calc_data,
						     vector->data.buf[0]);
			}

			/* Enqueue generated bit into calc_data */
			if (vector->cipher == ACVP_CFB1) {
				cfb_byte_for_next_round =
					calc_data.buf[calc_data.len - 16] & 1<<7;
				sym_mct_cfb1_enqueue(&calc_data,
						     vector->data.buf[0]);
			}
		}

		CKINT(sym_backend->mct_fini(vector, parsed_flags));

		/* Iterate over each write definition and invoke it. */
		for_each_testresult(processdata->testresult, entry, i)
			CKINT(write_one_entry(entry, single_mct_result,
					      parsed_flags));

		/* Append the output JSON stream with test results. */
		json_object_array_add(resultsarray, single_mct_result);

		if (vector->cipher == ACVP_CFB8 ||
		    vector->cipher == ACVP_CFB1) {
			for (k = 0; k < vector->key.len; k++)
				vector->key.buf[k] ^= calc_data.buf[k];

			/* Use the rightmost 16 bytes as new IV */
			memcpy(vector->iv.buf,
			       calc_data.buf + calc_data.len - vector->iv.len,
			       vector->iv.len);

			vector->data.buf[0] = cfb_byte_for_next_round;
		} else {
			/*
			 * AES MCT Key Shuffle - why does it need to be so
			 * inconsistent?
			 */
			if (vector->key.len == 16) {
				/* Take the 16 MSB from CT[j] */
				for (i = 0; i < 16; i++)
					vector->key.buf[i] ^=
						vector->data.buf[i];
			} else if (vector->key.len == 24) {
				/* Take the 8 LSB from CT[j-1] */
				for (i = 0; i < 8; i++)
					vector->key.buf[i] ^=
						calc_data.buf[calc_data.len - 8 + i];

				/* Take the 16 MSB from CT[j] */
				for (i = 0; i < 16; i++)
					vector->key.buf[i + 8] ^=
						vector->data.buf[i];
			} else if (vector->key.len == 32) {
				/* Take the 16 MSB from CT[j - 1] */
				for (i = 0; i < 16; i++)
					vector->key.buf[i] ^=
						calc_data.buf[i];
				/* Take the 16 MSB from CT[j] */
				for (i = 0; i < 16; i++)
					vector->key.buf[i + 16] ^=
						vector->data.buf[i];
			}
		}

		if (vector->cipher != ACVP_ECB &&
		    vector->cipher != ACVP_CFB8 &&
		    vector->cipher != ACVP_CFB1) {
			memcpy(vector->iv.buf, vector->data.buf, vector->iv.len);
			memcpy(vector->data.buf, calc_data.buf, vector->data.len);
		}
	}

	json_object_object_add(testresult, "resultsArray", resultsarray);
	/* Append the output JSON stream with test results. */
	json_object_array_add(testresults, testresult);

	/* We have written data, generic parser should not write it. */
	ret = FLAG_RES_DATA_WRITTEN;

out:
	if (ret && ret != FLAG_RES_DATA_WRITTEN) {
		sym_backend->mct_fini(vector, parsed_flags);
		if (resultsarray)
			json_object_put(resultsarray);
	}
	free_buf(&calc_data);

	return ret;
}

static int sym_aft_aes_decrypt_helper(const struct json_array *processdata,
			      flags_t parsed_flags,
			      struct json_object *testvector,
			      struct json_object *testresults,
			      int (*callback)(struct sym_data *vector,
					      flags_t parsed_flags),
			      struct sym_data *vector)
{
	int ret = 0;
	(void)processdata;
	(void)testvector;
	(void)testresults;

	CKINT(callback(vector, parsed_flags));
	/* Free the buffer that may be left by the backend. */
	if (vector->integrity_error)
		free_buf(&vector->data);

out:
	return ret;
}

static int sym_tdes_concatenate_keys(const struct json_array *processdata,
				     flags_t parsed_flags,
				     struct json_object *testvector,
				     struct json_object *testresults,
	int (*callback)(struct sym_data *vector, flags_t parsed_flags),
				     struct sym_data *vector)
{
	BUFFER_INIT(tmp);
	BUFFER_INIT(tmp2);
	int ret;

	(void)processdata;
	(void)testvector;
	(void)testresults;

	CKINT(alloc_buf(vector->key.len + vector->key2.len + vector->key3.len,
			&tmp));
	memcpy(tmp.buf, vector->key.buf, vector->key.len);
	memcpy(tmp.buf + vector->key.len, vector->key2.buf, vector->key2.len);
	memcpy(tmp.buf + vector->key.len + vector->key2.len, vector->key3.buf,
	       vector->key3.len);

	logger_binary(LOGGER_DEBUG, tmp.buf, tmp.len, "Concatenated key");

	/* save original key pointer */
	copy_ptr_buf(&tmp2, &vector->key);
	/* move new key pointer into vector->key */
	copy_ptr_buf(&vector->key, &tmp);
	CKINT(callback(vector, parsed_flags));

	/* restore original key pointer */
	copy_ptr_buf(&vector->key, &tmp2);
	free_buf(&tmp);

out:
	return ret;
}

static int sym_tdes_tester(struct json_object *in, struct json_object *out,
			   uint64_t cipher)
{
	struct sym_data vector;

	if (!sym_backend) {
		logger(LOGGER_WARN, "No symmetric cipher backend set\n");
		return -EOPNOTSUPP;
	}

	/* Referencing the backend functions */
	const struct sym_callback sym_encrypt_aft = { sym_backend->encrypt, &vector, sym_tdes_concatenate_keys};
	const struct sym_callback sym_decrypt_aft = { sym_backend->decrypt, &vector, sym_tdes_concatenate_keys};
	const struct sym_callback sym_encrypt_mct = { sym_backend->encrypt, &vector, sym_mct_tdes_helper};
	const struct sym_callback sym_decrypt_mct = { sym_backend->decrypt, &vector, sym_mct_tdes_helper};
	const struct json_callback sym_callback_aft[] = {
		{ .callback.sym = sym_encrypt_aft, CB_TYPE_sym, FLAG_OP_ENC | FLAG_OP_AFT},
		{ .callback.sym = sym_decrypt_aft, CB_TYPE_sym, FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_callbacks sym_callbacks_aft = SET_CALLBACKS(sym_callback_aft);

	const struct json_callback sym_callback_mct[] = {
		{ .callback.sym = sym_encrypt_mct, CB_TYPE_sym, FLAG_OP_ENC | FLAG_OP_MCT},
		{ .callback.sym = sym_decrypt_mct, CB_TYPE_sym, FLAG_OP_DEC | FLAG_OP_MCT},
	};
	const struct json_callbacks sym_callbacks_mct = SET_CALLBACKS(sym_callback_mct);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry sym_testresult_aft_entries[] = {
		{"ct",		{.data.buf = &vector.data, WRITER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"pt",		{.data.buf = &vector.data, WRITER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_testresult sym_testresult_aft = SET_ARRAY(sym_testresult_aft_entries, &sym_callbacks_aft);

	const struct json_entry sym_testresult_mct_entries[] = {
		/* Write IV for enc / dec during MCT processing */
		{"ct",		{.data.buf = &vector.data, WRITER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"pt",		{.data.buf = &vector.data, WRITER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},
		{"iv",		{.data.buf = &vector.iv, WRITER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"iv",		{.data.buf = &vector.iv, WRITER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},
	};
	const struct json_testresult sym_testresult_mct = SET_ARRAY(sym_testresult_mct_entries, &sym_callbacks_mct);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file. For example:
	 * {
         *   "tcId": 2171,
         *   "key": "1529BAC6229586F057FAA59353851686",
         *   "pt": ""
         * },
	 *
	 * After parsing each individual test vector, the test should be
	 * executed and the result should be written to a JSON file.
	 */
	const struct json_entry sym_test_aft_entries[] = {
		{"iv",		{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_AFT},
		{"key1",	{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"key2",	{.data.buf = &vector.key2, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"key3",	{.data.buf = &vector.key3, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"pt",		{.data.buf = &vector.data, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},

		{"iv",		{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_DEC | FLAG_OP_AFT},
		{"key1",	{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"key2",	{.data.buf = &vector.key2, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"key3",	{.data.buf = &vector.key3, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"ct",		{.data.buf = &vector.data, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},

		{"payloadLen",	{.data.integer = &vector.data_len_bits, PARSER_UINT},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_array sym_test_aft = SET_ARRAY(sym_test_aft_entries, &sym_testresult_aft);

	const struct json_entry sym_test_mct_entries[] = {
		{"iv",		{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_MCT},
		{"key1",	{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"key2",	{.data.buf = &vector.key2, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"key3",	{.data.buf = &vector.key3, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"pt",		{.data.buf = &vector.data, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},

		{"iv",		{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_DEC | FLAG_OP_MCT},
		{"key1",	{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},
		{"key2",	{.data.buf = &vector.key2, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},
		{"key3",	{.data.buf = &vector.key3, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},
		{"ct",		{.data.buf = &vector.data, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},

		{"payloadLen",	{.data.integer = &vector.data_len_bits, PARSER_UINT},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_DEC | FLAG_OP_MCT},
	};
	const struct json_array sym_test_mct = SET_ARRAY(sym_test_mct_entries, &sym_testresult_mct);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors. For example:
	 * {
	 *   "direction": "encrypt",
	 *   "testType" : "AFT",
	 *   "keyLen": 128,
	 *   "ivLen": 96,
         *   "tests": [
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry sym_testgroup_entries[] = {
		{"tests",	{.data.array = &sym_test_aft, PARSER_ARRAY},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"tests",	{.data.array = &sym_test_aft, PARSER_ARRAY},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"tests",	{.data.array = &sym_test_mct, PARSER_ARRAY},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"tests",	{.data.array = &sym_test_mct, PARSER_ARRAY},	FLAG_OP_DEC | FLAG_OP_MCT}
	};
	const struct json_array sym_testgroup = SET_ARRAY(sym_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data. For example:
	 * {
	 *   "vsId": 1564,
	 *   "algorithm": "AES-ECB",
	 *   "testGroups": [
	 */
	const struct json_entry sym_testanchor_entries[] = {
		{"testGroups",	{.data.array = &sym_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array sym_testanchor = SET_ARRAY(sym_testanchor_entries, NULL);

	memset(&vector, 0, sizeof(struct sym_data));
	vector.cipher = cipher;

	/* Process all. */
	return process_json(&sym_testanchor, "1.0", in, out);
}

static int sym_aes_tester(struct json_object *in, struct json_object *out,
			  uint64_t cipher)
{
	struct sym_data vector;

	if (!sym_backend) {
		logger(LOGGER_WARN, "No symmetric cipher backend set\n");
		return -EOPNOTSUPP;
	}

	/* Referencing the backend functions */
	const struct sym_callback sym_encrypt_aft = { sym_backend->encrypt, &vector, NULL};
	const struct sym_callback sym_decrypt_aft = { sym_backend->decrypt, &vector, sym_aft_aes_decrypt_helper};
	const struct sym_callback sym_encrypt_mct = { sym_backend->encrypt, &vector, sym_mct_aes_helper};
	const struct sym_callback sym_decrypt_mct = { sym_backend->decrypt, &vector, sym_mct_aes_helper};
	const struct json_callback sym_callback_aft[] = {
		{ .callback.sym = sym_encrypt_aft, CB_TYPE_sym, FLAG_OP_ENC | FLAG_OP_AFT},
		{ .callback.sym = sym_decrypt_aft, CB_TYPE_sym, FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_callbacks sym_callbacks_aft = SET_CALLBACKS(sym_callback_aft);

	const struct json_callback sym_callback_mct[] = {
		{ .callback.sym = sym_encrypt_mct, CB_TYPE_sym, FLAG_OP_ENC | FLAG_OP_MCT},
		{ .callback.sym = sym_decrypt_mct, CB_TYPE_sym, FLAG_OP_DEC | FLAG_OP_MCT},
	};
	const struct json_callbacks sym_callbacks_mct = SET_CALLBACKS(sym_callback_mct);

	/*
	 * Define which test result data should be written to the test result
	 * JSON file.
	 */
	const struct json_entry sym_testresult_aft_entries[] = {
		{"ct",		{.data.buf = &vector.data, WRITER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"pt",		{.data.buf = &vector.data, WRITER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"testPassed",	{.data.integer = &vector.integrity_error, WRITER_BOOL_TRUE_TO_FALSE},	FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_testresult sym_testresult_aft = SET_ARRAY(sym_testresult_aft_entries, &sym_callbacks_aft);

	const struct json_entry sym_testresult_mct_entries[] = {
		/* Write IV for enc / dec during MCT processing */
		{"ct",		{.data.buf = &vector.data, WRITER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"pt",		{.data.buf = &vector.data, WRITER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},
		{"iv",		{.data.buf = &vector.iv, WRITER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"iv",		{.data.buf = &vector.iv, WRITER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},
	};
	const struct json_testresult sym_testresult_mct = SET_ARRAY(sym_testresult_mct_entries, &sym_callbacks_mct);

	/*
	 * Define one particular test vector that is expected in the JSON
	 * file. For example:
	 * {
         *   "tcId": 2171,
         *   "key": "1529BAC6229586F057FAA59353851686",
         *   "pt": ""
         * },
	 *
	 * After parsing each individual test vector, the test should be
	 * executed and the result should be written to a JSON file.
	 */
	const struct json_entry sym_test_aft_entries[] = {
		{"iv",		{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_AFT},
		{"sequenceNumber",	{.data.integer = &vector.xts_sequence_no, PARSER_UINT},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_AFT},
		{"tweakValue",	{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_AFT},
		{"key",		{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"pt",		{.data.buf = &vector.data, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_AFT},

		{"iv",		{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_DEC | FLAG_OP_AFT},
		{"sequenceNumber",	{.data.integer = &vector.xts_sequence_no, PARSER_UINT},	FLAG_OPTIONAL | FLAG_OP_DEC | FLAG_OP_AFT},
		{"tweakValue",	{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_DEC | FLAG_OP_AFT},
		{"key",		{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"ct",		{.data.buf = &vector.data, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_AFT},

		{"payloadLen",	{.data.integer = &vector.data_len_bits, PARSER_UINT},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_DEC | FLAG_OP_AFT},
	};
	const struct json_array sym_test_aft = SET_ARRAY(sym_test_aft_entries, &sym_testresult_aft);

	const struct json_entry sym_test_mct_entries[] = {
		{"iv",		{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_MCT},
		{"key",		{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"pt",		{.data.buf = &vector.data, PARSER_BIN},	FLAG_OP_ENC | FLAG_OP_MCT},

		{"iv",		{.data.buf = &vector.iv, PARSER_BIN},	FLAG_OPTIONAL | FLAG_OP_DEC | FLAG_OP_MCT},
		{"key",		{.data.buf = &vector.key, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},
		{"ct",		{.data.buf = &vector.data, PARSER_BIN},	FLAG_OP_DEC | FLAG_OP_MCT},

		{"payloadLen",	{.data.integer = &vector.data_len_bits, PARSER_UINT},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_DEC | FLAG_OP_MCT},
	};
	const struct json_array sym_test_mct = SET_ARRAY(sym_test_mct_entries, &sym_testresult_mct);

	/*
	 * Define the test group which contains ancillary data and eventually
	 * the array of individual test vectors. For example:
	 * {
	 *   "direction": "encrypt",
	 *   "testType" : "AFT",
	 *   "keyLen": 128,
	 *   "ivLen": 96,
         *   "tests": [
	 *
	 * As this definition does not mark specific individual test vectors,
	 * the testresult entry is set to NULL.
	 */
	const struct json_entry sym_testgroup_entries[] = {
		{"kwCipher",	{.data.buf = &vector.kwcipher, PARSER_STRING},	FLAG_OPTIONAL | FLAG_OP_ENC | FLAG_OP_AFT },
		{"kwCipher",	{.data.buf = &vector.kwcipher, PARSER_STRING},	FLAG_OPTIONAL | FLAG_OP_DEC | FLAG_OP_AFT },
		{"tests",	{.data.array = &sym_test_aft, PARSER_ARRAY},	FLAG_OP_ENC | FLAG_OP_AFT},
		{"tests",	{.data.array = &sym_test_aft, PARSER_ARRAY},	FLAG_OP_DEC | FLAG_OP_AFT},
		{"tests",	{.data.array = &sym_test_mct, PARSER_ARRAY},	FLAG_OP_ENC | FLAG_OP_MCT},
		{"tests",	{.data.array = &sym_test_mct, PARSER_ARRAY},	FLAG_OP_DEC | FLAG_OP_MCT}
	};
	const struct json_array sym_testgroup = SET_ARRAY(sym_testgroup_entries, NULL);

	/*
	 * Define the anchor of the tests in the highest level of the JSON
	 * input data. For example:
	 * {
	 *   "vsId": 1564,
	 *   "algorithm": "AES-ECB",
	 *   "testGroups": [
	 */
	const struct json_entry sym_testanchor_entries[] = {
		{"testGroups",	{.data.array = &sym_testgroup, PARSER_ARRAY},	0},
	};
	const struct json_array sym_testanchor = SET_ARRAY(sym_testanchor_entries, NULL);

	if (!sym_backend) {
		logger(LOGGER_ERR,
		       "No backend implementation for symmetric ciphers available\n");
		return EOPNOTSUPP;
	}

	memset(&vector, 0, sizeof(struct sym_data));
	vector.cipher = cipher;

	/* Process all. */
	return process_json(&sym_testanchor, "1.0", in, out);
}

static struct cavs_tester sym_aes =
{
	0,
	ACVP_AESMASK,
	sym_aes_tester,	/* process_req */
	NULL
};

static struct cavs_tester sym_tdes =
{
	0,
	ACVP_TDESMASK,
	sym_tdes_tester,	/* process_req */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(register_sym)
static void register_sym(void)
{
	register_tester(&sym_aes, "Generic AES");
	register_tester(&sym_tdes, "Generic TDES");
}

void register_sym_impl(struct sym_backend *implementation)
{
	register_backend(sym_backend, implementation, "symmetric ciphers");
}
