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

#ifndef _PARSER_HMAC_H
#define _PARSER_HMAC_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief Keyed message digest (HMAC / CMAC) cipher data structure holding
 *	  the data for the cipher operations specified in hmac_backend
 *
 * @var key [in] Symmetric key for cipher operation in binary form.
 * @var key2 [disregard] Parser-internal use.
 * @var key3 [disregard] Parser-internal use.
 * @var msg [in] Data buffer holding the message to be hashed in binary form.
 * @var maclen [in] Length of the requested message digest in bits - depending
 *		    on the cipher requests, the message digest length may
 *		    deviate from the digest size.
 * @var mac [out] Message digest of the message in binary form.
 *		    Note, the backend must allocate the buffer of the right
 *		    size before storing data in it. The parser frees the memory.
 * @var verify_result [disregard] Please disregard this variable, it is used
 *				    by the parser.
 * @var cipher [in] Cipher specification as defined in cipher_definitions.h
 */
struct hmac_data {
	struct buffer key;
	struct buffer key2;
	struct buffer key3;
	struct buffer msg;
	uint32_t maclen;
	struct buffer mac;
	uint32_t verify_result;
	uint64_t cipher;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 * @var hmac_generate Perform a keyed message digest operation with the given
 *			data. Note, despite the name, HMAC and CMAC is covered
 *			by the callback.
 */

struct hmac_backend {
	int (*hmac_generate)(struct hmac_data *data, flags_t parsed_flags);
};

void register_hmac_impl(struct hmac_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_HMAC_H */
