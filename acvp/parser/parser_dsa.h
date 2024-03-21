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

#ifndef _PARSER_DSA_H
#define _PARSER_DSA_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief: Data structure exchanged with backend for PQG operation
 *
 * This data structure is used for PQ generation and verification with
 * provable and probable primes, In addition it is used for the canonical
 * and unverifiable G generation. This implies that some values are
 * used depending on the PQG operation type.
 *
 * The backend can analyze the requested PQG operation as follows (note,
 * a backend is not required to implement all operation types as they are
 * selected during test vector generation time):
 *
 *	parsed_flags &= ~FLAG_OP_GDT;
 *
 *	if (parsed_flags ==
 *	    (FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROBABLE_PQ_GEN))
 *		return pq_generation_probable_p_q;
 *	else if (parsed_flags ==
 *		 (FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROVABLE_PQ_GEN))
 *		return pq_generation_provable_p_q;
 *
 *	else if (parsed_flags ==
 *		 (FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROBABLE_PQ_GEN))
 *		return pq_verification_probable_p_q;
 *	else if (parsed_flags ==
 *		 (FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROVABLE_PQ_GEN))
 *		return pq_verification_provable_p_q;
 *
 *	else if (parsed_flags ==
 *		 (FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_UNVERIFIABLE_G_GEN))
 *		return unverifiable_g_generation;
 *	else if (parsed_flags ==
 *		 (FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_CANONICAL_G_GEN))
 *		return canonical_g_generation;
 *
 *	else if (parsed_flags ==
 *		 (FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_UNVERIFIABLE_G_GEN))
 *		return unverifiable_g_verification;
 *	else if (parsed_flags ==
 *		 (FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_CANONICAL_G_GEN))
 *		return canonical_g_verification;
 *
 *	else
 *		BUG();
 *
 * General note: all data buffers that are returned by the backend must be
 * allocated by the backend. The parser takes care of deallocating them.
 *
 * @var L [in] L size in bits
 * @var N [in] N size in bits
 * @var cipher [in] Hash type to use for PQG operation
 * @var P [out: PQ generation, in: G generation, in: PQG verification] domain
 *	    parameter P
 * @var Q [out: PQ generation, in: G generation, in: PQG verification] domain
 *	    parameter Q
 * @var G [out: G generation, in: PQG verification] domain parameter G
 *
 * @var domainseed [out: PQ generation, in: all other use cases] This
 *		   buffer holds the domain seed. It is filled in parallel with
 *		   with all seed variables below. As the seed variables below
 *		   are only used for separate, tests, they can all be collapsed
 *		   into one.
 *
 * @var g_canon_index [in: G generation, in: G verification] The index value
 * 			provided to the generator in canonical method. Only to
 * 			be used for canonical G generation / verification.
 * @var g_canon_domain_param_seed [in: G generation, in: G verification] The
 *				    seed used for the P and Q generation in
 *				    the probable method. Only to be used for
 *				    unverifiable G generation / verification.
 *				    DEPRECATED - use @var domainseed
 *
 * @var g_unver_domain_param_seed [in: G verification] The seed used for the P
 * 				    and Q generation in the unverifiable method.
 * 				    Only to be used for unverifiable G
 * 				    verification.
 *				    DEPRECATED - use @var domainseed
 * @var g_unver_h [in: G verification] The index value provided to the generator
 * 		    in unverifiable method. Only to be used for unverifiable G
 * 		    verification.
 *
 * @var pq_prob_counter [out: PQ generation, in: PQ verification] The counter
 *			  to be used for the probable P and Q generation. Only
 *			  to be used for PQ generation / verification with
 *			  probable primes.
 * @var pq_prob_domain_param_seed [out: PQ generation, in: PQ verification]
 *				    The seed used for the P and Q generation in
 *				    the probable method. Only to be used for
 *				    probable P/Q generation / verification.
 *				    DEPRECATED - use @var domainseed
 *
 * @var pq_prov_firstseed [out: PQ generation, in: PQ: verification]
 *			    Firstseed for PQ generation. Only to be used for PQ
 *			    generation / verification with provable primes.
 *			    DEPRECATED - use @var domainseed
 * @var pq_prov_pcounter [out: PQ generation, in: PQ verification] The counter
 *			   to be used for the provable P generation. Only to be
 *			   used for PQ generation / verification with provable
 *			   primes.
 * @var pq_prov_qcounter [out: PQ generation, in: PQ verification] The counter
 *			   to be used for the provable Q generation. Only to be
 *			   used for PQ generation / verification with provable
 *			   primes.
 * @var pq_prov_pseed [out] PQ generation, in: PQ verification] The seed
 *			to be used for the provable P generation. Only to be
 *			used for PQ generation / verification with provable
 *			primes.
 * @var pq_prov_qseed [out] PQ generation, in: PQ verification] The seed
 *			to be used for the provable Q generation. Only to be
 *			used for PQ generation / verification with provable
 *			primes.
 *
 * @var pqgver_success [out] for PQG verification only] Is PQ or G
 *			 verification with given parameters successful (1) or
 *			 whether it failed (0).
 */
struct dsa_pqg_data {
	uint32_t L;
	uint32_t N;
	uint64_t cipher;
	struct buffer P;
	struct buffer Q;
	struct buffer G;

	struct buffer domainseed;

	struct buffer g_canon_index;
	struct buffer g_canon_domain_param_seed;

	struct buffer g_unver_domain_param_seed;
	struct buffer g_unver_h;

	uint32_t pq_prob_counter;
	struct buffer pq_prob_domain_param_seed;

	struct buffer pq_prov_firstseed;
	uint32_t pq_prov_pcounter;
	uint32_t pq_prov_qcounter;
	struct buffer pq_prov_pseed;
	struct buffer pq_prov_qseed;

	uint32_t pqgver_success;
};

/**
 * @brief DSA PQG data structure holding the data for the cipher
 *	  operations specified with dsa_pqggen. It is also used to provide the
 *	  input data for key generation, signature generation and verification.
 *
 * General note: all data buffers that are returned by the backend must be
 * allocated by the backend. The parser takes care of deallocating them.
 *
 * @var cipher [in] Hash type to use for signature operation
 * @var safeprime [in] Safe prime definition (only set for SP800-56A rev 3)
 * @var L [in] L size in bits (only set for FIPS 186-4 / SP800-56A rev 1)
 * @var N [in] N size in bits (only set for FIPS 186-4 / SP800-56A rev 1)
 * @var P [out] domain parameter P (only set for FIPS 186-4 / SP800-56A rev 1)
 * @var Q [out] domain parameter Q (only set for FIPS 186-4 / SP800-56A rev 1)
 * @var G [out] domain parameter G (only set for FIPS 186-4 / SP800-56A rev 1)
 */
struct dsa_pqggen_data {
	uint64_t cipher;
	uint64_t safeprime;
	uint32_t L;
	uint32_t N;
	struct buffer P;
	struct buffer Q;
	struct buffer G;
};

/**
 * @brief DSA key generation data structure holding the data for the cipher
 *	  operations specified with dsa_keygen.
 *
 * General note: all data buffers that are returned by the backend must be
 * allocated by the backend. The parser takes care of deallocating them.
 *
 * The key generation covers the following cipher definitions:
 *	* FIPS 186-4 DSA key generation
 *	* SP800-56A rev 1 DH key generation
 *	* SP800-56A rev 3 DH key generation using safe primes
 *
 * @var pqg.L [in] L size in bits (only set for FIPS 186-4 / SP800-56A rev 1)
 * @var pqg.N [in] N size in bits (only set for FIPS 186-4 / SP800-56A rev 1)
 * @var pqg.P [in] domain parameter P (only set for FIPS 186-4 / SP800-56A rev 1)
 * @var pqg.Q [in] domain parameter Q (only set for FIPS 186-4 / SP800-56A rev 1)
 * @var pqg.G [in] domain parameter G (only set for FIPS 186-4 / SP800-56A rev 1)
 * @var pqg.safeprime [in] Safe prime definition (only set for SP800-56A rev 3)
 * @var X [out] private DSA key parameter X
 * @var Y [out] public DSA key parameter Y
 */
struct dsa_keygen_data {
	struct dsa_pqggen_data pqg;
	struct buffer X;
	struct buffer Y;
};

/**
 * @brief DSA key verification data structure holding the data for the cipher
 *	  operations specified with dsa_keygen.
 *
 * The key verification covers the following cipher definitions:
 *	* SP800-56A rev 3 DH key generation using safe primes
 *
 * @var pqg.safeprime [in] Safe prime definition (only set for SP800-56A rev 3)
 * @var X [in] private DSA key parameter X
 * @var Y [in] public DSA key parameter Y
 * @var keyver_success [out] Is DSA key verification with given parameters
 *			     successful (1) or whether it failed (0).
 */
struct dsa_keyver_data {
	struct dsa_pqggen_data pqg;
	struct buffer X;
	struct buffer Y;
	uint32_t keyver_success;
};

/**
 * @brief DSA signature generation data structure holding the data for the
 *	  cipher operations specified with dsa_siggen.
 *
 * NOTE: You MUST use the very same private key for the same modulo. That means
 *	 you generate a new DSA key when a new @var pqg value set is provided.
 *	 If the Y value of the data structure below is not filled,
 *	 you must copy the DSA.Y from your used key. To simplify the
 *	 entire key handling, you may implement the helper functions
 *	 registered with @var dsa_keygen_en and @var dsa_free_key below.
 *	 When using these functions, you must ensure that the DSA signature
 *	 generation is invoked single-threaded because the generated
 *	 DSA key and the Y parameter is stored in a global variable.
 *
 * General note: all data buffers that are returned by the backend must be
 * allocated by the backend. The parser takes care of deallocating them.
 *
 * @var cipher [in] Hash type to use for signature operation
 * @var msg [in] Message that shall be signed
 * @var pqg.L [in] L size in bits
 * @var pqg.N [in] N size in bits
 * @var pqg.P [out] domain parameter P
 * @var pqg.Q [out] domain parameter Q
 * @var pqg.G [out] domain parameter G
 * @var Y [out] public DSA key parameter Y
 * @var R [out] DSA signature parameter R
 * @var S [out] DSA signature parameter S
 * @var privkey [in] DSA private key to be used for signature generation.
 *		  This variable is only set if dsa_keygen_en callback provided.
 */
struct dsa_siggen_data {
	uint64_t cipher;
	struct buffer msg;
	struct dsa_pqggen_data pqg;
	struct buffer Y;
	struct buffer R;
	struct buffer S;
	void *privkey;
};

/**
 * @brief DSA signature verification data structure holding the data for the
 *	  cipher operations specified with dsa_sigver.
 *
 * General note: all data buffers that are returned by the backend must be
 * allocated by the backend. The parser takes care of deallocating them.
 *
 * @var pqg.L [in] L size in bits
 * @var pqg.N [in] N size in bits
 * @var cipher [in] Hash type to use for signature operation
 * @var msg [in] Message whose signature shall be verified
 * @var pqg.P [in] domain parameter P
 * @var pqg.Q [in] domain parameter Q
 * @var pqg.G [in] domain parameter G
 * @var Y [in] public DSA key parameter Y
 * @var R [in] DSA signature parameter R
 * @var S [in] DSA signature parameter S
 * @var sigver_success [out] Is DSA signature successfully verified (1) or
 *			 whether the verification failed (0).
 */
struct dsa_sigver_data {
	uint64_t cipher;
	struct buffer msg;
	struct dsa_pqggen_data pqg;
	struct buffer Y;
	struct buffer R;
	struct buffer S;
	uint32_t sigver_success;
};

/**
 * @brief Callback data structure that must be implemented by the backend. Some
 *	  callbacks only need to be implemented if the respective cipher support
 *	  shall be tested.
 *
 * All functions return 0 on success or != 0 on error. Note, a failure in the
 * DSA PQG verification @var dsa_pqg due to problematic input parameters is
 * expected. In such cases, a DSA PQG verification error is still considered to
 * be a successful operation and the return code should be 0. Similarly, the
 * signature verification callback @var dsa_sigver shall return 0 if the
 * signature verification fails. Only if some general error is detected a
 * return code != must be returned.
 *
 * @var dsa_keygen DSA key generation (FIPS 184-4 as well as SP800-56A rev 3
 *		   using safe primes)
 * @var dsa_keyver DSA key verfication (only for SP800-56A rev 3 using safe
 *		   primes)
 * @var dsa_siggen DSA signature generation
 * @var dsa_sigver DSA signature verification
 * @var dsa_pqg PQG generation and verification callback handler -- see
 *		  the documentation for dsa_pqg_data how the backend can
 *		  identify the PQG operation type.
 * @var dsa_pqggen Generic PQG generation functionality without specific
 *		     limitations or requirements.
 *
 * @var dsa_keygen_en This is an optional helper call to reduce the amount
 *			of code in the backend for signature generation. The
 *			ACVP protocol requires that the same DSA key is used
 *			for multiple signature generation operation. Yet,
 *			the module must generate the DSA key. To allow the
 *			ACVP Parser to manage the DSA key and invoke the
 *			DSA key generation, you may provide this function with
 *			the following parameters:
 *			@var pqg [in] Buffer holding the PQG information to
 *					generate the DSA key.
 *			@var Y [out] Buffer with the DSA public key.
 *			@var privkey [out] Provide the pointer to the RSA
 *				        private key.
 * @var dsa_free_key This function is required if dsa_keygen_en is registered.
 *		       This function is intended to free the private DSA key
 *		       handle created with dsa_keygen_en.
 */
struct dsa_backend {
	int (*dsa_keygen)(struct dsa_keygen_data *data, flags_t parsed_flags);
	int (*dsa_keyver)(struct dsa_keyver_data *data, flags_t parsed_flags);
	int (*dsa_siggen)(struct dsa_siggen_data *data, flags_t parsed_flags);
	int (*dsa_sigver)(struct dsa_sigver_data *data, flags_t parsed_flags);
	int (*dsa_pqg)(struct dsa_pqg_data *data, flags_t parsed_flags);
	int (*dsa_pqggen)(struct dsa_pqggen_data *data, flags_t parsed_flags);

	int (*dsa_keygen_en)(struct dsa_pqggen_data *pqg, struct buffer *Y,
			     void **privkey);
	void (*dsa_free_key)(void *privkey);
};

void register_dsa_impl(struct dsa_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_DSA_H */
