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

#ifndef _PARSER_FLAGS_H
#define _PARSER_FLAGS_H

#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

/*
 * Flags definition for the parser.
 *
 * These flags are obtained from the test vectors. They are used to
 * implement conditionals in either invocation of the callback functions,
 * the parsed fields, etc.
 *
 * Note, these flags are grouped considering that there will never be a mix
 * between these groups. This should guarantee that the flags field will be
 * sufficient in size.
 */

/* Datatype of the flags field. */
typedef uint64_t	flags_t;

/* Applicable to all implementations */
/* All Ciphers:  Algorithm Functional Tests */
#define FLAG_OP_AFT					(0x0000000000000001ULL)
/* All Ciphers:  Monte-Carlo Test */
#define FLAG_OP_MCT					(0x0000000000000002ULL)
/* RSA ciphers */
#define FLAG_OP_KAT					(0x0000000000000004ULL)
#define FLAG_OP_GDT					(0x0000000000000008ULL)
/* ECDH validation */
#define FLAG_OP_VAL					(0x0000000000000010ULL)
#define FLAG_OP_VOT					(0x0000000000000020ULL)
/* Hash operation */
#define FLAG_OP_LDT					FLAG_OP_VOT
#define FLAG_OP_MASK_BASE				(0x000000000000003fULL)

/* Symmetric Ciphers: JSON field is expected during enc. */
#define FLAG_OP_ENC					(0x0000000000000040ULL)
/* Symmetric Ciphers:  JSON field is expected during dec */
#define FLAG_OP_DEC					(0x0000000000000080ULL)
#define FLAG_OP_MASK_SYMMETRIC				(0x00000000000000c0ULL)

/* HMAC: CMAC generate test */
#define FLAG_OP_CMAC_GEN_TEST				(0x0000000000000100ULL)
/* HMAC: CMAC verify test */
#define FLAG_OP_CMAC_VER_TEST				(0x0000000000000200ULL)
/* MAC verify test */
#define FLAG_OP_MVT					(0x0000000000000400ULL)
#define FLAG_OP_MASK_MAC				(0x0000000000000f00ULL)

/* JSON field is expected for asymmetric keyGen operation */
#define FLAG_OP_ASYM_TYPE_KEYGEN			(0x0000000000001000ULL)
/* JSON field is expected for asymmetric keyVer operation */
#define FLAG_OP_ASYM_TYPE_KEYVER			(0x0000000000002000ULL)
/* JSON field is expected for asymmetric sigGen operation */
#define FLAG_OP_ASYM_TYPE_SIGGEN			(0x0000000000004000ULL)
/* JSON field is expected for asymmetric sigVer operation */
#define FLAG_OP_ASYM_TYPE_SIGVER			(0x0000000000008000ULL)
/* RSA: JSON field is expected for RSA legacy sigVer operation */
#define FLAG_OP_RSA_TYPE_LEGACY_SIGVER			(0x0000000000010000ULL)
/* RSA: JSON field is expected for RSA component signature primitive */
#define FLAG_OP_RSA_TYPE_COMPONENT_SIG_PRIMITIVE	(0x0000000000020000ULL)
/* RSA: JSON field is expected for RSA component dec primitive */
#define FLAG_OP_RSA_TYPE_COMPONENT_DEC_PRIMITIVE	(0x0000000000040000ULL)
#define FLAG_OP_ASYM_TYPE_MASK				(0x00000000000ff000ULL)

/* RSA signatures: JSON field is expected for RSA PKCS15 operation */
#define FLAG_OP_RSA_SIG_PKCS15				(0x0000000000100000ULL)
/* RSA signatures: JSON field is expected for RSA X9.31 operation */
#define FLAG_OP_RSA_SIG_X931				(0x0000000000200000ULL)
/* RSA signatures: JSON field is expected for RSA PKCS1 PSS operation */
#define FLAG_OP_RSA_SIG_PKCS1PSS			(0x0000000000400000ULL)
#define FLAG_OP_RSA_SIG_MASK				(0x0000000000f00000ULL)
/* RSA primes: provable primes (Appendix B.3.2) */
#define FLAG_OP_RSA_PQ_B32_PRIMES			(0x0000000001000000ULL)
/* RSA primes: probable primes (Appendix B.3.3) */
#define FLAG_OP_RSA_PQ_B33_PRIMES			(0x0000000002000000ULL)
/* RSA primes: provable primes (Appendix B.3.4) */
#define FLAG_OP_RSA_PQ_B34_PRIMES			(0x0000000004000000ULL)
/* RSA primes: provable/probable primes (Appendix B.3.5) */
#define FLAG_OP_RSA_PQ_B35_PRIMES			(0x0000000008000000ULL)
/* RSA primes: probable primes (Appendix B.3.6) */
#define FLAG_OP_RSA_PQ_B36_PRIMES			(0x0000000010000000ULL)
/* RSA prime test: Miller Rabin (Table C.2) */
#define FLAG_OP_RSA_PRIME_TEST_C2			(0x0000000020000000ULL)
/* RSA prime test: Miller Rabin (Table C.3) */
#define FLAG_OP_RSA_PRIME_TEST_C3			(0x0000000040000000ULL)
#define FLAG_OP_RSA_CRT					(0x0000000080000000ULL)
#define FLAG_OP_MASK_RSA				(0x00000000fffff000ULL)

/* SHA: Bitwise or Bytewise representation */
#define FLAG_OP_SHA_BITWISE				(0x0000000100000000ULL)
#define FLAG_OP_SHA_BYTEWISE				(0x0000000200000000ULL)
/* SHA: Empty message included? */
#define FLAG_OP_SHA_EMPTY_MSG				(0x0000000400000000ULL)
#define FLAG_OP_MASK_SHA				(0x0000000f00000000ULL)

/* ECDH: Scheme specification */
#define FLAG_OP_ECDH_SCHEME_FULL_UNIFIED		(0x0000001000000000ULL)
#define FLAG_OP_ECDH_SCHEME_FULL_MQV			(0x0000002000000000ULL)
#define FLAG_OP_ECDH_SCHEME_EPHEMERAL_UNIFIED		(0x0000004000000000ULL)
#define FLAG_OP_ECDH_SCHEME_ONE_PASS_UNIFIED		(0x0000008000000000ULL)
#define FLAG_OP_ECDH_SCHEME_ONE_PASS_MQV		(0x0000010000000000ULL)
#define FLAG_OP_ECDH_SCHEME_ONE_PASS_DH			(0x0000020000000000ULL)
#define FLAG_OP_ECDH_SCHEME_STATIC_UNIFIED		(0x0000040000000000ULL)
#define FLAG_OP_ECDH_SCHEME_ECCDH_COMPONENT_TEST	(0x0000080000000000ULL)

/* KAS Scheme is part of FLAG_OP_MASK_ECDH *and* FLAG_OP_MASK_DH!!!! */
#define FLAG_OP_KAS_SCHEME_TEST				(0x0000100000000000ULL)

#define FLAG_OP_MASK_ECDH				(0x00001ff000000000ULL)

/*
 * DH: Scheme specification - reuse of ECDH flags as both will not occur at
 * same time.
 */
#define FLAG_OP_DH_SCHEME_DH_HYBRID1			(0x0000002000000000ULL)
#define FLAG_OP_DH_SCHEME_MQV2				(0x0000004000000000ULL)
#define FLAG_OP_DH_SCHEME_EPHEMERAL			(0x0000008000000000ULL)
#define FLAG_OP_DH_SCHEME_HYBRID_ONE_FLOW		(0x0000010000000000ULL)
#define FLAG_OP_DH_SCHEME_MQV1				(0x0000020000000000ULL)
#define FLAG_OP_DH_SCHEME_ONE_FLOW			(0x0000040000000000ULL)
#define FLAG_OP_DH_SCHEME_STATIC			(0x0000080000000000ULL)
#define FLAG_OP_MASK_DH					(0x00001ff000000000ULL)

/* KAS ROLE and ECDH/DH Scheme are in parallel, but not with ECDSA */
#define FLAG_OP_KAS_ROLE_INITIATOR			(0x0001000000000000ULL)
#define FLAG_OP_KAS_ROLE_RESPONDER			(0x0002000000000000ULL)

/* ECDSA: key generation type */
/* key generation with extra entropy (FIPS 186-4 B.4.1) */
#define FLAG_OP_ECDSA_SECRETGENTYPE_EXTRABITS		(0x0000100000000000ULL)
/* key generation with testing candidates (FIPS 186-4 B.4.2) */
#define FLAG_OP_ECDSA_SECRETGENTYPE_TESTING		(0x0000200000000000ULL)
/* DSA: PQG component testing (generation and verification) */
#define FLAG_OP_DSA_TYPE_PQGGEN				(0x0000400000000000ULL)
#define FLAG_OP_DSA_TYPE_PQGVER				(0x0000800000000000ULL)
#define FLAG_OP_DSA_PROBABLE_PQ_GEN			(0x0001000000000000ULL)
#define FLAG_OP_DSA_PROVABLE_PQ_GEN			(0x0002000000000000ULL)
#define FLAG_OP_DSA_UNVERIFIABLE_G_GEN			(0x0004000000000000ULL)
#define FLAG_OP_DSA_CANONICAL_G_GEN			(0x0008000000000000ULL)
#define FLAG_OP_DSA_PQG_TYPES_MASK			(0x000f000000000000ULL)

#define FLAG_OP_KDF_TYPE_TLS				(0x0010000000000000ULL)
#define FLAG_OP_KDF_TYPE_SSH				(0x0020000000000000ULL)
#define FLAG_OP_KDF_TYPE_IKEV2				(0x0040000000000000ULL)
#define FLAG_OP_KDF_TYPE_IKEV1				(0x0080000000000000ULL)
#define FLAG_OP_KDF_TYPE_IKEV1_PSK			(0x0100000000000000ULL)
#define FLAG_OP_KDF_TYPE_IKEV1_DSA			(0x0200000000000000ULL)
#define FLAG_OP_KDF_TYPE_IKEV1_PKE			(0x0400000000000000ULL)
#define FLAG_OP_KDF_TYPE_800_108			(0x0800000000000000ULL)
#define FLAG_OP_KDF_TYPE_HKDF				(0x1000000000000000ULL)
#define FLAG_OP_KDF_TYPE_ANSI_X963			(0x2000000000000000ULL)
#define FLAG_OP_KDF_TYPE_SRTP				(0x4000000000000000ULL)

/* DRBG other input flag */
#define FLAG_OP_DRBG_RESEED				(0x2000000000000000ULL)
#define FLAG_OP_DRBG_GENERATE				(0x4000000000000000ULL)

/* TLS v1.3 flags */
#define FLAG_OP_TLS13_RUNNING_MODE_DHE			(0x0000000000001000ULL)
#define FLAG_OP_TLS13_RUNNING_MODE_PSK			(0x0000000000002000ULL)
#define FLAG_OP_TLS13_RUNNING_MODE_PSKDHE		(0x0000000000004000ULL)

/* Mask of the fields that can be found in entries */
#define FLAG_OP_MASK					(0x7fffffffffffffffULL)

/* Flags that are only set in the parser code */
/* Optional entry */
#define FLAG_OPTIONAL					(0x8000000000000000ULL)

#ifdef __cplusplus
}
#endif

#endif /* _PARSER_FLAGS_H */
