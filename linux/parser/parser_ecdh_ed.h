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

#ifndef _PARSER_ECDH_ED_H
#define _PARSER_ECDH_ED_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief ECDH based on Edwards Curve KDF Shared Secret generation
 *
 * @var cipher [in] ED curve
 * @var pub_rem [in] Remote public key
 * @var priv_rem [in] Remote private key
 * @var pub_loc [out] Local public key
 * @var kdfz [out] KDFed shared secret
 */
struct ecdh_ed_ss_data {
	uint64_t cipher;
	struct buffer pub_rem;
	struct buffer priv_rem;
	struct buffer pub_loc;
	struct buffer kdfz;
};

/**
 * @brief ECC hashed Shared Secret verification
 *
 * @var cipher [in] ED curve
 * @var pub_rem [in] Remote public key
 * @var priv_rem [in] Remote private key
 * @var pub_loc [in] Local public key
 * @var priv_loc [in] Local private key
 * @var kdfz [in] KDFed shared secret
 * @var validity_success [out] Does the generated shared secret match with
 *				 @var hashzz (true - 1) or not (false - 0).
 */
struct ecdh_ed_ss_ver_data {
	uint64_t cipher;
	struct buffer pub_rem;
	struct buffer priv_rem;
	struct buffer pub_loc;
	struct buffer priv_loc;
	struct buffer kdfz;
	uint32_t validity_success;
};

/**
 * @brief Callback data structure that must be implemented by the backend. Some
 *	  callbacks only need to be implemented if the respective cipher support
 *	  shall be tested.
 *
 * All functions return 0 on success or != 0 on error. Note, a failure in the
 * validity check @var ecdh_ed_ss_ver due to a mismatch between the expected
 * and the actual shared secret is expected. In such cases, the validity test
 * error is still considered to be a successful operation and the return code
 * should be 0. Only if some general error is
 * detected a return code != must be returned.
 *
 * @var ecdh_ed_ss ED shared secret generation
 * @var ecdh_ed_ss_ver ED shared secret verification
 */
struct ecdh_ed_backend {
	int (*ecdh_ed_ss)(struct ecdh_ed_ss_data *data,
			  flags_t parsed_flags);
	int (*ecdh_ed_ss_ver)(struct ecdh_ed_ss_ver_data *data,
			      flags_t parsed_flags);
};

void register_ecdh_ed_impl(struct ecdh_ed_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_ECDH_ED_H */
