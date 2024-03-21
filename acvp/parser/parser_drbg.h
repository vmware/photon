/*
 * Copyright (C) 2015 - 2022, Stephan Mueller <smueller@chronox.de>
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

#ifndef _PARSER_DRBG_H
#define _PARSER_DRBG_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief DRBG cipher data structure holding the data for the cipher
 *	  operations specified in drbg_backend.
 *
 * All variables and how they are applied with the DRBG implementation are
 * documented in the CAVS specification for the DRBG.
 *
 * @var entropy [in] Buffer holding the entropy string in binary form.
 * @var nonce [in] Buffer holding the nonce string in binary form.
 * @var pers [in] Buffer holding the personalization string in binary form.
 * @var addtl_reseed [in]
 * 		Data structure holding the additional input string to be used
 *		for the reseed operation before the random number generation
 *		operation. It is allowed to to contain NULL entries when no
 *		additional data is required.
 * @var entropy_reseed [in]
 *		Data structure holding the entropy input string to be used for
 *		the reseed operation before the random number generation. It is
 *		allowed to to contain NULL entries when no entropy data is
 *		required.
 * @var addtl_generate [in]
 *			Data structure holding the additional input string in
 *		 	for the prediction resistance operation in binary form.
 *			This data structure holds two buffers for the first and
 *			second reseed operation. The first buffer corresponds
 *			with the first reseed and the second buffer corresponds
 *			with the second reseed. It is allowed to to contain NULL
 *			entries when no additional data is required.
 * @var entropy_generate [in]
 *			  Data structure holding the entropy input string in
 *			  for the prediction resistance operation in binary
 *			  form. This data structure holds two buffers for the
 *			  first and second reseed operation. The first buffer
 *			  corresponds with the first reseed and the second
 *			  buffer corresponds with the second reseed. It is
 *			  allowed to to contain NULL entries when no
 *			  entropy data is required.
 * @var random [out] The buffer to hold the generated random number in binary
 *		       form (buffer must be allocated by the backend, and the
 *		       parser releases the buffer).
 * @var type [in] DRBG type - DRBGCTR or DRBGHASH or DRBGHMAC
 * @var cipher [in] Cipher specification as defined in cipher_definitions.h.
 *				 * AES128
 *				 * AES192
 *				 * AES256
 *				 * SHA1
 *				 * SHA224
 *				 * SHA256
 *				 * SHA384
 *				 * SHA512
 *				 * SHA512224
 *				 * SHA512256
 *				 * SHA1
 *				 * SHA224
 *				 * SHA256
 *				 * SHA384
 *				 * SHA512
 *				 * SHA512224
 *				 * SHA512256
 *				 * ACVP_CIPHERTYPE_TDES (the mode is irrelevant
 *							 when specifying TDES)
 * @var rnd_data_bits_len [in] Length of random data to produce in bits.
 * @var pr [in] Prediction resistance enabled (1 == true, 0 == false)
 * @var df [in] Derivation function requested (1 == true, 0 == false)
 */
struct drbg_data {
	struct buffer entropy;
	struct buffer nonce;
	struct buffer pers;
	struct buffer_array addtl_reseed;
	struct buffer_array entropy_reseed;
	struct buffer_array addtl_generate;
	struct buffer_array entropy_generate;
	struct buffer random;
	uint64_t type;
	uint64_t cipher;
	uint32_t rnd_data_bits_len;
	uint32_t pr;
	uint32_t df;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 * @var drbg_generate Perform a DRBG random number generation operation with
 *			the given data.
 */
struct drbg_backend {
	int (*drbg)(struct drbg_data *data, flags_t parsed_flags);
};

void register_drbg_impl(struct drbg_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_DRBG_H */
