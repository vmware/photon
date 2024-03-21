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

#ifndef _PARSER_SYM_H
#define _PARSER_SYM_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief Symmetric cipher data structure holding the data for the cipher
 *	  operations specified in sym_backend
 *
 * @var key [in] Symmetric key for cipher operation in binary form
 * @var key2 [disregard] Please disregard this buffer
 * @var key3 [disregard] Please disregard this buffer
 * @var iv [in] IV for the cipher operation in binary form. It may be empty
 *		  for ciphers that do not support IVs (like AES-ECB or AES-KW).
 *		  Note, for XTS, this buffer contains the tweak value.
 * @var cipher [in] Cipher specification as defined in cipher_definitions.h
 * @var data [in/out] Buffer with input data that is also expected to hold
 *			the result data. Note, if the buffer size needs to be
 *			different for the output data than for the input
 *			data, the backend must change the buffer as needed.
 *			The buffer is freed by the parser.
 * @var data_len_bits [in] Length of input data in bits. This value is
 *			     used for CFB-1 where only some bits out of a byte
 *			     is relevant for testing.
 * @var xts_sequence_no [in] If XTS sequence number is requested, it is
 *			       stored in this variable. In this case, the IV
 *			       is NULL.
 * @var inner_loop_final_cj1[out] This value is optional and contains the final
 * 				  C[j-1] cipher text from the inner loop for
 *				  AES. If this value is set the inner loop of
 *				  the MCT testing implemented in the parser is
 *				  skipped and only the outer loop is performed.
 *				  If the backend does not implement the inner
 *				  loop (which is assumed to be the default),
 *				  this buffer should not be touched by the
 *				  backend.
 * @var integrity_error [out] This variable is to be filled by the backend
 *			      during a decryption operation to indicate
 *			      whether the decryption was successful (0 value)
 *			      or whether an integrity error occurred (value
 *			      of 1). Note, in this case, the @var data
 *			      buffer should be released.
 * @var kwcipher [in] KW type - Inverse or Cipher
 * @var priv [storage] This pointer allows the backend to store private data
 *			 like a pointer to a cipher handle allocated during
 *			 the init call and used during update or fini calls.
 *			 The backend must deallocate the resources during fini
 *			 call.
 */
struct sym_data {
	struct buffer key;
	struct buffer key2;
	struct buffer key3;
	struct buffer iv;
	uint64_t cipher;
	struct buffer data;
	uint32_t data_len_bits;
	uint32_t xts_sequence_no;
	struct buffer inner_loop_final_cj1;
	uint32_t integrity_error;
	struct buffer kwcipher;
	void *priv;
};

/**
 * @brief Callback data structure that must be implemented by the backend. Some
 *	  callbacks only need to be implemented if the respective cipher support
 *	  shall be tested.
 *
 * All functions return 0 on success or != 0 on error. Note, if an
 * authenticating cipher returns an integrity error during decryption, the data
 * buffer with the return data must contain the value of
 * CIPHER_DECRYPTION_FAILED with CIPHER_DECRYPTION_FAILED_LEN buffer size. Yet
 * the return code MUST be 0 as test vectors deliberately provide data with
 * integrity errors.
 *
 * @var encrypt Callback implementing the encrypt operation using the
 *		  @var data buffer. The @var parsed_flags point to flags
 *		  specified in parser_flags.h.
 * @var decrypt Callback implementing the decrypt operation using the
 *		  @var data buffer. The @var parsed_flags point to flags
 *		  specified in parser_flags.h.

 * MCT testing implies that a cipher handle with its state is
 * initialized and then kept alive for successive cipher operations.
 * I.e. if a block chaining mode other than ECB is used, the state
 * of the block chaining mode must be retained.
 * Each cipher operation must perform the requested
 * encryption/decryption operation on the current cipher handle state
 * and return the ciphertext/plaintext.
 *
 * @var mct_init Initialize the cipher handle. The @var parsed_flags contain
 *		   either FLAG_OP_ENC or FLAG_OP_DEC for encryption/decryption.
 *		   The allocated cipher handle may be stored in the priv
 *		   pointer.
 * @var mct_update Perform a crypto operation on the cipher handle and
 *		     return the result of the crypto operation.
 * @var mct_fini Free all resources pertaining the cipher operation.
 */
struct sym_backend {
	int (*encrypt)(struct sym_data *data, flags_t parsed_flags);
	int (*decrypt)(struct sym_data *data, flags_t parsed_flags);

	int (*mct_init)(struct sym_data *data, flags_t parsed_flags);
	int (*mct_update)(struct sym_data *data, flags_t parsed_flags);
	int (*mct_fini)(struct sym_data *data, flags_t parsed_flags);
};

void register_sym_impl(struct sym_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_SYM_H */
