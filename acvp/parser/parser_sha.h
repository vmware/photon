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

#ifndef _PARSER_SHA_H
#define _PARSER_SHA_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief Hash cipher data structure holding the data for the cipher
 *	  operations specified in sha_backend
 *
 * @var msg [in] Data buffer holding the message to be hashed in binary form.
 * @var bitllen [in] Size of the message in bits - NOTE the @var msg is a
 *		       buffer containing the message in full bytes. If the
 *		       request for message sizes are made that are not full
 *		       buffers, the @var bitlen field can be consulted to
 *		       identify the number of rightmost bits to be pulled from
 *		       @var msg. @var bitlen is per definition at most 7
 *		       bits smaller than the message buffer in @var msg and
 *		       never larger.
 * @var ldt_expansion_size [in] If this value is larger than zero, the msg
 *				data provided must be repeated until this
 *				the amount of bits defined in
 *				ldt_expansion_size is reached. Note, the
 *				expansion of the msg data MUST be done
 *				PRIOR to invoking the hash operation, as the
 *				test is intended to verify that the hash
 *				implementation can handle large data during
 *				its processing. Note, this variable is only
 *				set if an LDT test vector was requested.
 *				Commonly this can be achieved by simply calling
 *				the hash update function with the following loop
 *				`for (i = 0; i < data->ldt_expansion_size; i += data->msg.len)`
 * @var outlen [in] Size of the output message digest to be created in bits.
 *		      This field is required for variable-sized output message
 *		      digests, such as SHAKE.
 * @var minoutlen [in] MinimumOutputLength as defined for the SHAKE MCT. Note,
 *			 this value is only used for the MCT operation and does
 *			 not need to be considered by a backend.
 * @var maxoutlen [in] MaximumOutputLength as defined for the SHAKE MCT. Note,
 *			 this value is only used for the MCT operation and does
 *			 not need to be considered by a backend.
 * @var mac [out] Message digest of the message in binary form.
 *		    Note, the backend must allocate the buffer of the right
 *		    size before storing data in it. The parser frees the memory.
 * @var cipher [in] Cipher specification as defined in cipher_definitions.h
 */
struct sha_data {
	struct buffer msg;
	uint32_t bitlen;
	uint64_t ldt_expansion_size;
	uint32_t outlen;
	uint32_t minoutlen;
	uint32_t maxoutlen;
	struct buffer mac;
	uint64_t cipher;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 * @var hash_generate Perform a message digest operation with the given data.
 * @var hash_mct_inner_loop Perform inner loop of the hash MCT. The returned
 *	message digest buffer must contain the data of the last iteration.
 *	Note: SHA1/2 have a different MCT definition compared to SHAKE and
 *	SHA3! If this pointer is set to NULL, the parser will perform the
 *	task of executing the MCT using the hash_generate function. Thus, this
 *	callback is a convenience callback to allow developers the reduction of
 *	the number of invocations of an IUT.
 *	Note 2: If this function returns an error, the parser will fall back
 *	to use hash_generate. This way it is possible to implement an innner
 *	loop in the IUT for, say, SHA1/2 but not for SHA3.
 */
struct sha_backend {
	int (*hash_generate)(struct sha_data *data, flags_t parsed_flags);
	int (*hash_mct_inner_loop)(struct sha_data *data, flags_t parsed_flags);
};

void register_sha_impl(struct sha_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_SHA_H */
