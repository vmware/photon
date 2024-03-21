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

#ifndef _PARSER_ECDSA_H
#define _PARSER_ECDSA_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief ECDSA key generation data structure holding the data for the cipher
 *	  operations specified in ecdsa_keygen. This test is used
 *	  for FIPS 186-4 B.4.2 (ECDSA key generation with testing candiates)
 *	  tests as specified in the ECDSA CAVS specification.
 *
 * @var d [out] ECDSA private key point
 * @var Qx [out] ECDSA affine x coordinate of public point Q
 * @var Qy [out] ECDSA affine y coordinate of public point Q
 * @var cipher [in] Cipher pointing to the curve
 */
struct ecdsa_keygen_data {
	struct buffer d;
	struct buffer Qx;
	struct buffer Qy;
	uint64_t cipher;
};

/**
 * @brief ECDSA key generation data structure holding the data for the cipher
 *	  operations specified in ecdsa_keygen_extra. This test is used
 *	  for FIPS 186-4 B.4.1 (ECDSA key generation with extra entropy)
 *	  tests as specified in the ECDSA CAVS specification.
 *
 * @var d [out] ECDSA private key point
 * @var Qx [out] ECDSA affine x coordinate of public point Q
 * @var Qy [out] ECDSA affine y coordinate of public point Q
 * @var cipher [in] Cipher pointing to the curve
 */
struct ecdsa_keygen_extra_data {
	struct buffer d;
	struct buffer Qx;
	struct buffer Qy;
	uint64_t cipher;
};

/**
 * @brief ECDSA key verification data structure holding the data for the cipher
 *	  operations specified in ecdsa_pkvver.
 *
 * @var Qx [in] ECDSA affine x coordinate of public point Q
 * @var Qy [in] ECDSA affine y coordinate of public point Q
 * @var cipher [in] Cipher pointing to the curve
 * @var keyver_success [out] Is ECDSA key verification with given parameters
 *			       successful (1) or whether it failed (0).
 */
struct ecdsa_pkvver_data {
	struct buffer Qx;
	struct buffer Qy;
	uint64_t cipher;
	uint32_t keyver_success;
};

/**
 * @brief ECDSA signature generation data structure holding the data for the
 *	  signature generation operation. This test is specified in the ECDSA
 *	  CAVS specification.
 *
 * This data structure is also used for the ECDSA signature generation
 * primitive testing where @var msg is the already hashed message.
 *
 * NOTE: You MUST use the very same private key for the same curve. That means
 *	 you generate a new ECDSA key when a new curve in @var cipher value is
 *	 provided. If the Qx and Qy values of the data structure below are not
 *	 filled, you must copy the Qx and Qy from you used key. To simplify the
 *	 entire key handling, you may implement the helper functions
 *	 registered with @var ecdsa_keygen_en and @var ecdsa_free_key below.
 *	 When using these functions, you must ensure that the ECDSA signature
 *	 generation is invoked single-threaded because the generated
 *	 ECDSA key and the Qx and Qy parameter are stored in a global variable.
 *
 * @var msg [in] Plaintext message to be signed.
 * @var Qx [in/out] ECDSA affine x coordinate of public point Q that was used
 *		      to sign the message
 * @var Qy [in/out] ECDSA affine y coordinate of public point Q that was used
 *		      to sign the message
 * @var R [out] R part of the generated ECDSA signature
 * @var S [out] S part of the generated ECDSA signature
 * @var component [in] Is vector an ECDSA component testing (1) or a full
 *		       ECDSA signature testing (0)
 * @var cipher [in] Curve and hash algorithm to be used for ECDSA signature
 *		      generation.
 * @var privkey [in] ECDSA private key to be used for signature generation.
 *		  This variable is only set if ecdsa_keygen_en callback
 *		  provided.
 */
struct ecdsa_siggen_data {
	struct buffer msg;
	struct buffer Qx;
	struct buffer Qy;
	struct buffer R;
	struct buffer S;
	uint32_t component;
	uint64_t cipher;
	void *privkey;
};

/**
 * @brief ECDSA signature verification data structure holding the data for the
 *	  signature verification operation. This test is specified in the ECDSA
 *	  CAVS specification.
 *
 * This data structure is also used for the ECDSA signature verification
 * primitive testing where @var msg is the already hashed message.
 *
 * @var msg [in] Plaintext message to be signature verified.
 * @var Qx [in] ECDSA affine x coordinate of public point Q that was used to
 *		  sign the message
 * @var Qy [in] ECDSA affine y coordinate of public point Q that was used to
 *		  sign the message
 * @var R [in] R part of the ECDSA signature to be verified
 * @var S [in] S part of the ECDSA signature to be verified
 * @var component [in] Is vector an ECDSA component testing (1) or a full
 *		       ECDSA signature testing (0)
 * @var cipher [in] Curve and hash algorithm to be used for ECDSA signature
 *		    generation.
 * @var sigver_success [out] Is ECDSA signature verification with given
 *			     parameters successful (1) or whether it
 *			     failed (0).
 */
struct ecdsa_sigver_data {
	struct buffer msg;
	struct buffer Qx;
	struct buffer Qy;
	struct buffer R;
	struct buffer S;
	uint32_t component;
	uint64_t cipher;
	uint32_t sigver_success;
};

/**
 * @brief Callback data structure that must be implemented by the backend. Some
 *	  callbacks only need to be implemented if the respective cipher support
 *	  shall be tested.
 *
 * All functions return 0 on success or != 0 on error. Note, a failure in the
 * ECDSA key verification @var ecdsa_pkvver due to problematic input
 * parameters is expected. In such cases, an ECDSA key verification error is
 * still considered to be a successful operation and the return code should be
 * 0. Similarly, the signature verification callback @var ecdsa_sigver shall
 * return 0 if the signature verification fails. Only if some general error is
 * detected a return code != must be returned.
 *
 * @var ecdsa_keygen ECDSA key generation for B.4.2 testing candidates
 * @var ecdsa_keygen_extra ECDSA key generation for B.4.1 with extra entropy
 * @var ecdsa_pkvver ECDSA key verification
 * @var ecdsa_siggen ECDSA signature generation
 * @var ecdsa_sigver ECDSA signature verification
 *
 * @var ecdsa_keygen_en This is an optional helper call to reduce the amount
 *			of code in the backend for signature generation. The
 *			ACVP protocol requires that the same ECDSA key is used
 *			for multiple signature generation operation. Yet,
 *			the module must generate the ECDSA key. To allow the
 *			ACVP Parser to manage the ECDSA key and invoke the
 *			ECDSA key generation, you may provide this function with
 *			the following parameters:
 *			@var curve [in] Curve of the ECDSA key to generate.
 *			@var qx [out] Qx affine parameter of ECDSA key
 *			@var qx [out] Qy affine parameter of ECDSA key
 *			@var privkey [out] Provide the pointer to the ECDSA
 *				        private key.
 * @var ecdsa_free_key This function is required if ecdsa_keygen_en is
 * 			 registered. This function is intended to free the
 *			 private ECDSA key handle created with ecdsa_keygen_en.
 */
struct ecdsa_backend {
	int (*ecdsa_keygen)(struct ecdsa_keygen_data *data,
			    flags_t parsed_flags);
	int (*ecdsa_keygen_extra)(struct ecdsa_keygen_extra_data *data,
				  flags_t parsed_flags);
	int (*ecdsa_pkvver)(struct ecdsa_pkvver_data *data,
			    flags_t parsed_flags);
	int (*ecdsa_siggen)(struct ecdsa_siggen_data *data,
			    flags_t parsed_flags);
	int (*ecdsa_sigver)(struct ecdsa_sigver_data *data,
			    flags_t parsed_flags);

	int (*ecdsa_keygen_en)(uint64_t curve, struct buffer *qx,
			       struct buffer *qy, void **privkey);
	void (*ecdsa_free_key)(void *privkey);
};

/**
 * @brief Helper function to obtain the required buffer length for d, Qx and Qy
 *	  when to be generated by the backend.
 */
void ecdsa_get_bufferlen(uint64_t curve, size_t *dlen,
			 size_t *xlen, size_t *ylen);

void register_ecdsa_impl(struct ecdsa_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_ECDSA_H */
