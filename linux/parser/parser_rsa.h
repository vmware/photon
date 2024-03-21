/*
 * Copyright (C) 2017 - 2022, Stephan Mueller <smueller@chronox.de>
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

#ifndef _PARSER_RSA_H
#define _PARSER_RSA_H

#include "parser.h"
#include "parser_flags.h"

#ifdef __cplusplus
extern "C"
{
#endif

/**
 * @brief RSA key generation data structure holding the data for the cipher
 *	  operations specified in rsa_keygen_prime_data. This test is used
 *	  for FIPS 186-4 B.3.3 tests as specified in the RSA CAVS specification
 *	  section 6.2.2.2.
 *
 * @var modulus [in] RSA modulus in bits
 * @var p [in] RSA P parameter
 * @var q [in] RSA Q parameter
 * @var e [in] RSA exponent
 * @var keygen_success [out] Is RSA key generation with given parameters
 *			       successful (1) or whether it failed (0).
 */
struct rsa_keygen_prime_data {
	uint32_t modulus; /* input: modulus size in bits */
	struct buffer p; /* input */
	struct buffer q; /* input */
	struct buffer e; /* input */
	uint32_t keygen_success;
};

/**
 * @brief RSA key generation data structure holding the data for the cipher
 *	  operations specified in rsa_keygen_data. This test is used
 *	  for FIPS 186-4 B.3.4/5/6 tests as specified in the RSA CAVS
 *	  specification section 6.2.2.1.
 *
 * @var modulus [in] RSA modulus in bits
 * @var n [out] RSA N parameter. Buffer must be allocated by module and is
 *		  released by parser.
 * @var d [out] RSA D parameter. Buffer must be allocated by module and is
 *		  released by parser.
 * @var p [out] RSA P parameter. Buffer must be allocated by module and is
 *		  released by parser.
 * @var q [out] RSA Q parameter. Buffer must be allocated by module and is
 *		  released by parser.
 * @var e [in/out] RSA exponent as input. If this buffer is empty (only when
 *		     random e is supported by the module), the module
 *		     generates the random e value, allocates memory for this
 *		     buffer and places it into this buffer.
 *
 * The following buffers are for B.3.6 key generation.
 * @var xp [out]
 * @var xp1 [out]
 * @var xp2 [out]
 * @var xq [out]
 * @var xq1 [out]
 * @var xq2 [out]
 * @var bitlen [out]
 *
 * The following buffers are for CRT key format.
 * NOTE: These values must only be set when the key format is CRT. A backend can
 * use the parsed_flags to check if FLAG_OP_RSA_CRT is present.
 * @var dmp1 [out]
 * @var dmq1 [out]
 * @var iqmp [out]
 */
struct rsa_keygen_data {
	uint32_t modulus;
	struct buffer n;
	struct buffer d;
	struct buffer p;
	struct buffer q;
	struct buffer e;

	struct buffer xp;
	struct buffer xp1;
	struct buffer xp2;
	struct buffer xq;
	struct buffer xq1;
	struct buffer xq2;
	unsigned int bitlen[4];

	struct buffer dmp1;
	struct buffer dmq1;
	struct buffer iqmp;
};

/**
 * @brief RSA key generation data structure holding the data for the cipher
 *	  operations specified in rsa_keygen_prov_prime_data. This test is used
 *	  for FIPS 186-4 B.3.2 tests as specified in the RSA CAVS specification
 *	  section 6.2.1.
 *
 * @var modulus [in] RSA modulus in bits.
 * @var n [out] RSA N parameter. Buffer must be allocated by module and is
 *		  released by parser.
 * @var d [out] RSA D parameter. Buffer must be allocated by module and is
 *		  released by parser.
 * @var p [out] RSA P parameter. Buffer must be allocated by module and is
 *		  released by parser.
 * @var q [out] RSA Q parameter. Buffer must be allocated by module and is
 *		  released by parser.
 * @var seed [out] RSA random seed parameter used to generate the RSA key.
 *		     Buffer must be allocated by module and is released by
 *		     parser.
 * @var e [in/out] RSA exponent as input. If this buffer is empty (only when
 *		     random e is supported by the module), the module
 *		     generates the random e value, allocates memory for this
 *		     buffer and places it into this buffer.
 * @var cipher [in] Hash algorithm to be used for RSA key generation.
 */
struct rsa_keygen_prov_prime_data {
	unsigned int modulus;
	struct buffer n;
	struct buffer d;
	struct buffer p;
	struct buffer q;
	struct buffer seed;
	struct buffer e;
	uint64_t cipher;
};

/**
 * @brief RSA signature generation data structure holding the data for the
 *	  signature generation operation. This test is specified in the RSA CAVS
 *	  specification section 6.3.
 *
 * NOTE: You MUST use the very same private key for the same modulo. That means
 *	 you generate a new RSA key when a new @var modulo value is provided.
 *	 If the n and e values of the data structure below are not filled,
 *	 you must copy the RSA.e and RSA.n from you used key. To simplify the
 *	 entire key handling, you may implement the helper functions
 *	 registered with @var rsa_keygen_en and @var rsa_free_key below.
 *	 When using these functions, you must ensure that the RSA signature
 *	 generation is invoked single-threaded because the generated
 *	 RSA key and the n and e parameter are stored in a global variable.
 *
 * @var cipher [in] Hash algorithm to be used for RSA signature generation.
 * @var modulus [in] RSA modulus in bits.
 * @var saltlen [in] Length of salt for RSA PSS.
 * @var e [in/out] RSA exponent as input. If this buffer is empty (only when
 *		     random e is supported by the module), the module
 *		     generates the random e value, allocates memory for this
 *		     buffer and places it into this buffer.
 * @var msg [in] Plaintext message to be signed.
 * @var sig [out] Signature generated by the module. Buffer must be allocated
 *		    by module and is released by parser.
 * @var n [in/out] RSA N parameter. Buffer must be allocated by module and is
 *		     released by parser.
 * @var privkey [in] RSA private key to be used for signature generation.
 *		  This variable is only set if rsa_keygen_en callback provided.
 */
struct rsa_siggen_data {
	uint64_t cipher;
	uint32_t modulus;
	uint32_t saltlen;
	struct buffer e;
	struct buffer msg;
	struct buffer sig;
	struct buffer n;
	void *privkey;
};

/**
 * @brief RSA signature verification data structure holding the data for the
 *	  signature verification operation. This test is specified in the RSA
 *	  CAVS specification section 6.4.
 *
 * @var n [in] RSA modulus
 * @var e [in] RSA exponent
 * @var msg [in] Plaintext message to be signed.
 * @var sig [in] Signature of message to be verified.
 * @var modulus [in] RSA modulus in bits
 * @var saltlen [in] Length of salt for RSA PSS.
 * @var cipher [in] Hash algorithm to be used for RSA signature generation.
 * @var sig_result [out] Is RSA signature successfully verified (1) or
 *			   whether the verification failed (0).
 */
struct rsa_sigver_data {
	struct buffer n;
	struct buffer e;
	struct buffer msg;
	struct buffer sig;
	uint32_t modulus;
	uint32_t saltlen;
	uint64_t cipher;
	uint32_t sig_result;
};

/**
 * @brief  RSA signaturePrimitive mode capabilities (otherwise known as
 * 	   RSASP1 in [RFC3447])
 *
 * In this mode, the only tested capability is the correct exponentiation of
 * 's = msg^d mod n', where 'msg' is a message between '0' and 'n - 1',
 * 'd' is the private exponent and 'n' is the modulus, all supplied by the
 * testing ACVP server.
 *
 * @var msg [in] Message between 0 and n - 1
 * @var n [in] RSA modulus
 * @var d [in] RSA private exponent
 * @var e [in] RSA e
 * @var signature [out] RSA signature of a successful operation
 * @var sig_result [out] Is RSA signature operation successful (1) or not (0).
 */
struct rsa_signature_primitive_data {
	struct buffer msg;
	struct buffer n;
	struct buffer d;
	struct buffer e;
#if 0
	union {
		struct rsa_regular {
			struct buffer d;
		} rsa_regular;
		struct rsa_crt {
			struct buffer dmp1;
			struct buffer dmq1;
			struct buffer iqmp;
		} rsa_crt;
	} u;
#endif
	struct buffer signature;
	uint32_t sig_result;
};

/**
 * @brief RSA decrptionPrimitive mode capabilities (otherwise known as
 *	  RSADP1 in [RFC3447])
 *
 *  In this mode, the only tested capability is the correct exponentiation
 * 's = cipherText^d mod n', where 'cipherText' is a cipherText to be decrypted,
 * 'd' is the private exponent and 'n' is the modulus.  See [SP800-56B],
 *  Section 7.1.2 for details.
 *
 * In testing, only 'cipherText' is supplied by the ACVP server.  The
 * client is responsible for generating RSA key pairs of modulus 'n',
 * private key 'd', and calculates 's'.
 *
 * @var modulus [in] RSA modulus in bits
 * @var num [in] Number of test cases (used internally by the parser, disregard)
 * @var num_failures [in] Number of failing RSA keys (used internally by the
 *			  parser, disregard)
 * @var tcid [in] (internal usage)
 * @var msg [in] Message (or cipherText) to be decrypted.
 * @var n [out] RSA modulus - if rsa_keygen_en is set, buffer is filled with
 *			      the output of that call
 * @var e [out] RSA exponent - if rsa_keygen_en is set, buffer is filled with
 *			       the output of that call
 * @var s [out] Result of the decryption operation
 * @var dec_result [out] Is RSA decryption operation successful (1) or not (0).
 * @var privkey [in] RSA private key to be used for signature generation.
 *	 	     This variable is only set if rsa_keygen_en callback
 *		     provided.
 */
struct rsa_decryption_primitive_data {
	uint32_t modulus;
	uint32_t num;
	uint32_t num_failures;
	uint32_t tcid;
	struct buffer msg;
	struct buffer n;
	struct buffer e;
	struct buffer s;
	uint32_t dec_result;
	void *privkey;
};

/**
 * @brief Callback data structure that must be implemented by the backend. Some
 *	  callbacks only need to be implemented if the respective cipher support
 *	  shall be tested.
 *
 * All functions return 0 on success or != 0 on error. Note, a failure in the
 * RSA key generation @var rsa_keygen_prime due to problematic input
 * parameters is expected. In such cases, an RSA key generation error is still
 * considered to be a successful operation and the return code should be 0.
 * Similarly, the signature verification callback @var rsa_sigver shall
 * return 0 if the signature verification fails. Only if some general error is
 * detected a return code != must be returned.
 *
 * @var rsa_keygen RSA key generation for B.3.3 (CAVS test specification
 * 		     section 6.2.2.1)
 * @var rsa_siggen RSA signature generation
 * @var rsa_sigver RSA signature verification
 * @var rsa_keygen_prime RSA key generation for B.3.3 (CAVS test
 *			   specification 6.2.2.2)
 * @var rsa_keygen_prov_prime RSA key generation for B.3.2 (CAVS test
 *				specification section 6.2.1).
 *
 * @var rsa_keygen_en This is an optional helper call to reduce the amount
 *			of code in the backend for signature generation. The
 *			ACVP protocol requires that the same RSA key is used
 *			for multiple signature generation operation. Yet,
 *			the module must generate the RSA key. To allow the
 *			ACVP Parser to manage the RSA key and invoke the
 *			RSA key generation, you may provide this function with
 *			the following parameters:
 *			@var ebuf [in/out] Buffer holding public exponent. If
 *				  the buffer is empty (e.len == 0), the module
 *				  is requested to generate e and store it
 *				  in this buffer.
 *			@var modulus [in] Modulus size of the RSA key to
 *					  generate.
 *			@var privkey [out] Provide the pointer to the RSA
 *				        private key.
 *			@var nbuf [out] Buffer filled with the public RSA
 *					modulus.
 * @var rsa_free_key This function is required if rsa_keygen_en is registered.
 *		       This function is intended to free the private RSA key
 *		       handle created with rsa_keygen_en.
 */
struct rsa_backend {
	int (*rsa_keygen)(struct rsa_keygen_data *data, flags_t parsed_flags);
	int (*rsa_siggen)(struct rsa_siggen_data *data, flags_t parsed_flags);
	int (*rsa_sigver)(struct rsa_sigver_data *data, flags_t parsed_flags);
	int (*rsa_keygen_prime)(struct rsa_keygen_prime_data *data,
				flags_t parsed_flags);
	int (*rsa_keygen_prov_prime)(struct rsa_keygen_prov_prime_data *data,
				     flags_t parsed_flags);

	int (*rsa_keygen_en)(struct buffer *ebuf, uint32_t modulus,
			     void **privkey, struct buffer *nbuf);
	void (*rsa_free_key)(void *privkey);

	int (*rsa_signature_primitive)(struct rsa_signature_primitive_data *data,
				       flags_t parsed_flags);
	int (*rsa_decryption_primitive)(struct rsa_decryption_primitive_data *data,
				       flags_t parsed_flags);
};

void register_rsa_impl(struct rsa_backend *implementation);

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_RSA_H */
