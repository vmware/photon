/*
 * Copyright (C) 2019 - 2022, Stephan Mueller <smueller@chronox.de>
 *
 * License: see LICENSE file
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT KDF_108LL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 */

#ifndef _PARSER_PBKDF_H
#define _PARSER_PBKDF_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief PBKDF data structure
 *
 * @var hash [in] hash to be used for the KDF - note, the backend must
 *		    use the hash to initialize the HMAC cipher as required by
 *		    the PBKDF specification.
 * @var derived_key_length [in] Length of the derived key material to be
 *				  produced by the KDF in bits.
 * @var iteration_count [in] Number of iterations to be performed by PBKDF
 * @var password [in] Password to derive key from - note, the buffer contains
 *			the password string (i.e. ASCII-printable characters).
 *			The password->len value contains the size of the
 *			password including the terminating zero. If you need
 *			the size of the string, use strlen(password->buf) or
 *			password->len - 1.
 * @var salt [in] Salt required for PBKDF.
 * @var derived_key [out] The derived keying material output.
 */
struct pbkdf_data {
	uint64_t hash;
	uint32_t derived_key_length;
	uint32_t iteration_count;
	struct buffer password;
	struct buffer salt;
	struct buffer derived_key;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 * @var pbkdf Perform a PBKDF key derivation
 */
struct pbkdf_backend {
	int (*pbkdf)(struct pbkdf_data *data, flags_t parsed_flags);
};

void register_pbkdf_impl(struct pbkdf_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_PBKDF_H */
