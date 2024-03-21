/*
 * Copyright (C) 2015 - 2022, Stephan Mueller <smueller@chronox.de>
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

#ifndef _PARSER_KDF_108_H
#define _PARSER_KDF_108_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief SP800-108 KDF data structure
 *
 * @var mac [in] HMAC / CMAC to be used for the KDF
 * @var kdfmode [in] Mode of the KDF of one of the following flags:
 *		       ACVP_KDF_108_DOUBLE_PIPELINE
 *		       ACVP_KDF_108_FEEDBACK
 *		       ACVP_KDF_108_COUNTER
 * @var counter_location [in] Location of the counter specified with one
 *				of the following flags:
 *				ACVP_KDF_108_AFTER_FIXED
 *				ACVP_KDF_108_BEFORE_FIXED
 *				ACVP_KDF_108_MIDDLE_FIXED
 *				ACVP_KDF_108_BEFORE_ITERATOR
 * @var counter_length [in] Length of counter to be used in bits
 * @var derived_key_length [in] Length of the derived key material to be
 *				  produced by the KDF in bits.
 * @var key [in] Key derivation key
 * @var iv [in] For feedback mode KDF, use this IV.
 * @var break_location [out] The bit location in the fixed_data where
 *				the counter is placed. This is only needed for
 *				ACVP_KDF_108_MIDDLE_FIXED test vectors.
 * @var fixed_data [out] Fixed input data string - this can be an arbitrary
 *			 string that is used as label/counter input. The
 *			 backend / IUT must generate that string and return
 *			 it.
 *			 NOTE: It may be provided as input for regression
 *			 testing.
 * @var derived_key [out] The derived keying material output.
 */
struct kdf_108_data {
	uint64_t mac;
	uint64_t kdfmode;
	uint64_t counter_location;
	uint32_t counter_length;
	uint32_t derived_key_length;
	struct buffer key;
	struct buffer iv;
	uint32_t break_location;
	struct buffer fixed_data;
	struct buffer derived_key;
};

/**
 * @brief Callback data structure that must be implemented by the backend.
 *
 * All functions return 0 on success or != 0 on error.
 *
 * @var kdf_108 Perform an SP800-108 key derivation
 */
struct kdf_108_backend {
	int (*kdf_108)(struct kdf_108_data *data, flags_t parsed_flags);
};

void register_kdf_108_impl(struct kdf_108_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_KDF_108_H */
