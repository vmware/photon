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

#ifndef _PARSER_ECDH_H
#define _PARSER_ECDH_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief ECC CDH primitive and hashed Shared Secret generation
 *
 * @var cipher [in] ECC curve containing an OR of: one curve out of
 * 		      CURVEMASK, one hash out of HASHMASK, one MAC out
 * 		      of HMACMASK when using KDF
 * @var Qxrem [in] affine X coordinate of remote pubkey
 * @var Qyrem [in] affine Y coordinate of remote pubkey
 * @var privloc [disregard]
 * @var Qxloc [out] affine X coordinate of local pubkey
 * @var Qyloc [out] affine Y coordinate of local pubkey
 * @var hashzz [out] hashed shared secret / raw shared secret for ECC CDH
 */
struct ecdh_ss_data {
	uint64_t cipher;
	struct buffer Qxrem;
	struct buffer Qyrem;
	struct buffer privloc;
	struct buffer Qxloc;
	struct buffer Qyloc;
	struct buffer hashzz;
};

/**
 * @brief ECC hashed Shared Secret verification
 *
 * @var cipher [in] ECC curve containing an OR of: one curve out of
 * 		      CURVEMASK, one hash out of HASHMASK, one MAC out
 * 		      of HMACMASK
 * @var Qxrem [in] affine X coordinate of remote pubkey
 * @var Qzrem [in] affine Y coordinate of remote pubkey
 * @var privloc [in] private local key
 * @var Qxloc [in] affine X coordinate of local pubkey
 * @var Qyloc [in] affine Y coordinate of local pubkey
 * @var hashzz [in] hashed shared secret / raw shared secret for ECC CDH
 * @var validity_success [out] Does the generated shared secret match with
 *				 @var hashzz (true - 1) or not (false - 0).
 */
struct ecdh_ss_ver_data {
	uint64_t cipher;
	struct buffer Qxrem;
	struct buffer Qyrem;
	struct buffer privloc;
	struct buffer Qxloc;
	struct buffer Qyloc;
	struct buffer hashzz;
	uint32_t validity_success;
};

/**
 * @brief Callback data structure that must be implemented by the backend. Some
 *	  callbacks only need to be implemented if the respective cipher support
 *	  shall be tested.
 *
 * All functions return 0 on success or != 0 on error. Note, a failure in the
 * validity check @var ecdh_ss_ver due to a mismatch between the expected
 * and the actual shared secret is expected. In such cases, the validity test
 * error is still considered to be a successful operation and the return code
 * should be 0. Only if some general error is
 * detected a return code != must be returned.
 *
 * @var ecdh_ss ECC shared secret generation
 * @var ecdh_ss_ver ECC shared secret verification
 */
struct ecdh_backend {
	int (*ecdh_ss)(struct ecdh_ss_data *data, flags_t parsed_flags);
	int (*ecdh_ss_ver)(struct ecdh_ss_ver_data *data, flags_t parsed_flags);
};

void register_ecdh_impl(struct ecdh_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_ECDH_H */
