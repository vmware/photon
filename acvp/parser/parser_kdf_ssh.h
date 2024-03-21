/*
 * Copyright (C) 2018 - 2022, Stephan Mueller <smueller@chronox.de>
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

#ifndef _PARSER_KDF_SSH_H
#define _PARSER_KDF_SSH_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief SSH PRF testing context
 *
 * @var cipher [in] Hash algorithm to be used for PRF as well as symmetric
 *		      cipher reference which is to be used to determine the
 *		      key and IV length for the output. For the symmetric
 *		      cipher, use the following code to parse it:
 *
 * switch (data->cipher & ACVP_SYMMASK) {
 *	case ACVP_AES128:
 *		enclen = 16;
 *		ivlen = 16;
 *		break;
 *	case ACVP_AES192:
 *		enclen = 24;
 *		ivlen = 16;
 *		break;
 *	case ACVP_AES256:
 *		enclen = 32;
 *		ivlen = 16;
 *		break;
 *	case ACVP_TDESECB:
 *		enclen = 24;
 *		ivlen = 8;
 *		break;
 *	default:
 *		logger(LOGGER_WARN, "Cipher not identified\n");
 *		ret = -EINVAL;
 *		goto out;
 *	}
 *
 *		     The hash can be parsed with the following code:
 *
 * switch (data->cipher & ACVP_HASHMASK) {
 *	case ACVP_SHA1:
 *		maclen = 20;
 *		break;
 *	case ACVP_SHA256:
 *		maclen = 32;
 *		break;
 *	case ACVP_SHA384:
 *		maclen = 48;
 *		break;
 *	case ACVP_SHA512:
 *		maclen = 64;
 *		break;
 *	default:
 *		logger(LOGGER_WARN, "Mac not identified\n");
 *		ret = -EINVAL;
 *		goto out;
 *	}
 *
 * @var k [in] Shared secret buffer - note, this is in MPINT format
 * @var h [in] Hash data buffer
 * @var session_id [in] Session ID buffer
 * @var initial_iv_client [out] IV to be used by client
 * @var encryptiion_key_client [out] Symmetric encryption key to be used by
 *				 client
 * @var integrity_key_client [out] Key for integrity mechanism to be used by
 *			       client
 * @var initial_iv_server [out] IV to be used by server
 * @var encryptiion_key_server [out] Symmetric encryption key to be used by
 *				 server
 * @var integrity_key_server [out] Key for integrity mechanism to be used by
 *			       server
 */
struct kdf_ssh_data {
	uint64_t cipher;
	struct buffer k;
	struct buffer h;
	struct buffer session_id;
	struct buffer initial_iv_client;
	struct buffer encryption_key_client;
	struct buffer integrity_key_client;
	struct buffer initial_iv_server;
	struct buffer encryption_key_server;
	struct buffer integrity_key_server;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 * @var kdf_ssh Invoke the SSH PRF testing.
 */

struct kdf_ssh_backend {
	int (*kdf_ssh)(struct kdf_ssh_data *data, flags_t parsed_flags);
};

void register_kdf_ssh_impl(struct kdf_ssh_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_KDF_SSH_H */
