/*
 * Copyright (C) 2015 - 2022, Stephan Mueller <smueller@chronox.de>
 *
 * License: see LICENSE file
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT HKDFLL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 */

#ifndef _PARSER_HKDF_H
#define _PARSER_HKDF_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief RFC5869 KDF data structure
 *
 * @var hash [in] hash to be used for the KDF - note, the backend must
 *		    use the hash to initialize the HMAC cipher as required by
 *		    the HKDF specification.
 * @var dkmlen [in] Length of output keying material in bits
 * @var z [in] Shared secret (input key material)
 * @var salt [in] salt for the HKDF
 * @var info [in] Additional information for the HKDF
 * @var dkm [in/out] The derived keying material (if buffer is non-NULL, a
		     the backend shall validate the DKM with its own data
		     and report via @val validity_success - if the buffer is
		     NULL, the generated DKM is to be returned)
 * @var validity_success [out] Does the derived key material match with
 *			 @var dkm (1) or whether it does not match (0).
 *
 * @var fixed_info_pattern [disregard]
 * @var fi_partyU [disregard]
 * @var fi_partyU_ephem [disregard]
 * @var fi_partyV [disregard]
 * @var fi_partyV_ephem [disregard]
 */
struct hkdf_data {
	uint64_t hash;
	uint32_t dkmlen;
	struct buffer z;
	struct buffer salt;
	struct buffer info;
	struct buffer dkm;
	uint32_t validity_success;

	struct buffer fixed_info_pattern;
	struct buffer fi_partyU;
	struct buffer fi_partyU_ephem;
	struct buffer fi_partyV;
	struct buffer fi_partyV_ephem;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 * @var hkdf Perform an SP800-108 key derivation
 */
struct hkdf_backend {
	int (*hkdf)(struct hkdf_data *data, flags_t parsed_flags);
};

void register_hkdf_impl(struct hkdf_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_HKDF_H */
