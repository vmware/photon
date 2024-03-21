/*
 * Copyright 2021-2022 VMware, Inc.
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

#ifndef _PARSER_KMAC_H
#define _PARSER_KMAC_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief KECCAK Message Authentication Code (KMAC) cipher data structure holding
 *	  the data for the cipher operations specified in kmac_backend
 *
 * @var key [in] Symmetric key for cipher operation in binary form.
 * @var msg [in] Data buffer holding the message to be hashed in binary form.
 * @var maclen [in] Length of the requested message digest in bits - depending
 *		    on the cipher requests, the message digest length may
 *		    deviate from the digest size.
 * @val keylen [in] The length of key
 * @var mac [out] Message digest of the message in binary form.
 *		    Note, the backend must allocate the buffer of the right
 *		    size before storing data in it. The parser frees the memory.
 * @val customization [in] optional customization bit string of any length.
 *			   Note, the parser already converts the test data
 *			   into the right format. I.e. if the test vector
 *			   defines a hexadecimal buffer, the parser converts
 *			   it automatically into binary. If it is a string
 *			   the customization string is found in the buffer.
 *			   The IUT simply has to consume the provided buffer
 *			   without performing any conversion operation.
 * @var verify_result [out] This variable is to be filled by the backend
 *			    during a Verification test whether verification was
 *			    successful or not.
 * @val xof_enabled [in] eXtendable-Output filled to enable XOF mode or not
 * @var cipher [in] Cipher specification as defined in cipher_definitions.
 *
 * @var hex_customization [internal] Ignore
 */
struct kmac_data {
	struct buffer key;
	struct buffer msg;
	uint32_t maclen;
	uint32_t keylen;
	struct buffer mac;
	struct buffer customization;
	uint32_t verify_result;
	uint32_t xof_enabled;
	uint64_t cipher;

	uint32_t hex_customization;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 */

struct kmac_backend {
	int (*kmac_generate)(struct kmac_data *data, flags_t parsed_flags);
	int (*kmac_ver)(struct kmac_data *data, flags_t parsed_flags);
};

void register_kmac_impl(struct kmac_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_KMAC_H */
