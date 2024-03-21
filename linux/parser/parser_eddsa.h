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

#ifndef _PARSER_EDDSA_H
#define _PARSER_EDDSA_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief EDDSA key generation data structure holding the data for the cipher
 *	  operations specified in eddsa_keygen. This test is used
 *	  for FIPS 186-4 B.4.2 (EDDSA key generation with testing candiates)
 *	  tests as specified in the EDDSA CAVS specification.
 *
 * @var d [out] EDDSA private key point
 * @var q [out] EDDSA coordinate of public point Q
 * @var cipher [in] Cipher pointing to the curve
 */
struct eddsa_keygen_data {
	struct buffer d;
	struct buffer q;
	uint64_t cipher;
};

/**
 * @brief EDDSA key verification data structure holding the data for the cipher
 *	  operations specified in eddsa_pkvver.
 *
 * @var q [in] ED public key
 * @var d [in] ED private key
 * @var cipher [in] Cipher pointing to the curve
 * @var keyver_success [out] Is EDDSA key verification with given parameters
 *			       successful (1) or whether it failed (0).
 */
struct eddsa_keyver_data {
	struct buffer q;
	struct buffer d;
	uint64_t cipher;
	uint32_t keyver_success;
};

/**
 * @brief EDDSA signature generation data structure holding the data for the
 *	  signature generation operation. This test is specified in the EDDSA
 *	  CAVS specification.
 *
 * NOTE: You MUST use the very same private key for the same modulo. That means
 *	 you generate a new EDDSA key when a new curve in @var cipher is
 *	 provided. If the q value of the data structure below are not filled,
 *	 you must copy the EDDSA.q from you used key. To simplify the
 *	 entire key handling, you may implement the helper functions
 *	 registered with @var eddsa_keygen_en and @var eddsa_free_key below.
 *	 When using these functions, you must ensure that the EDDSA signature
 *	 generation is invoked single-threaded because the generated
 *	 EDDSA key and the n and e parameter are stored in a global variable.
 *
 * @var msg [in] Plaintext message to be signed.
 * @var q [out] EDDSA coordinate of public point Q that was used to
 *		  sign the message
 * @var signature [out] generated EDDSA signature
 * @var cipher [in] Curve and hash algorithm to be used for EDDSA signature
 *		      generation.
 * @var privkey [in] EDDSA private key to be used for signature generation.
 *		  This variable is only set if eddsa_keygen_en callback
 *		  provided.
 */
struct eddsa_siggen_data {
	struct buffer msg;
	struct buffer q;
	struct buffer signature;
	uint64_t cipher;
	void *privkey;
};

/**
 * @brief EDDSA signature verification data structure holding the data for the
 *	  signature verification operation. This test is specified in the EDDSA
 *	  CAVS specification.
 *
 * @var msg [in] Plaintext message to be signature verified.
 * @var q [in] EDDSA coordinate of public point Q that was used to
 *		 sign the message
 * @var signature [in] EDDSA signature to be verified
 * @var cipher [in] Curve and hash algorithm to be used for EDDSA signature
 *		      generation.
 * @var sigver_success [out] Is EDDSA signature verification with given
 *			       parameters successful (1) or whether it
 *			       failed (0).
 */
struct eddsa_sigver_data {
	struct buffer msg;
	struct buffer q;
	struct buffer signature;
	uint64_t cipher;
	uint32_t sigver_success;
};

/**
 * @brief Callback data structure that must be implemented by the backend. Some
 *	  callbacks only need to be implemented if the respective cipher support
 *	  shall be tested.
 *
 * All functions return 0 on success or != 0 on error. Note, a failure in the
 * EDDSA key verification @var eddsa_pkvver due to problematic input
 * parameters is expected. In such cases, an EDDSA key verification error is
 * still considered to be a successful operation and the return code should be
 * 0. Similarly, the signature verification callback @var eddsa_sigver shall
 * return 0 if the signature verification fails. Only if some general error is
 * detected a return code != must be returned.
 *
 * @var eddsa_keygen EDDSA key generation
 * @var eddsa_keyver EDDSA key verification
 * @var eddsa_siggen EDDSA signature generation
 * @var eddsa_sigver EDDSA signature verification
 *
 * @var eddsa_keygen_en This is an optional helper call to reduce the amount
 *			  of code in the backend for signature generation. The
 *			  ACVP protocol requires that the same EDDSA key is used
 *			  for multiple signature generation operation. Yet,
 *			  the module must generate the EDDSA key. To allow the
 *			  ACVP Parser to manage the EDDSA key and invoke the
 *			  EDDSA key generation, you may provide this function with
 *			  the following parameters:
 *			@var qbuf [in/out] Buffer holding the EDDSA public
 *				    key. If the buffer is empty (e.len == 0),
 *				    the module is requested to generate q and
 *				    store it in this buffer.
 *			@var curve [in] Curve of the EDDSA key to generate.
 *			@var privkey [out] Provide the pointer to the EDDSA
 *				        private key.
 * @var eddsa_free_key This function is required if eddsa_keygen_en is
 *			 registered. This function is intended to free the
 *			 private EdDSA key handle created with eddsa_keygen_en.
 */
struct eddsa_backend {
	int (*eddsa_keygen)(struct eddsa_keygen_data *data,
			    flags_t parsed_flags);
	int (*eddsa_keyver)(struct eddsa_keyver_data *data,
			    flags_t parsed_flags);
	int (*eddsa_siggen)(struct eddsa_siggen_data *data,
			    flags_t parsed_flags);
	int (*eddsa_sigver)(struct eddsa_sigver_data *data,
			    flags_t parsed_flags);

	int (*eddsa_keygen_en)(struct buffer *qbuf, uint64_t curve,
			       void **privkey);
	void (*eddsa_free_key)(void *privkey);
};

void register_eddsa_impl(struct eddsa_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_EDDSA_H */
