/*
 * Copyright (C) 2018 - 2022, Stephan Müller <smueller@chronox.de>
 * Copyright 2022 VMware, Inc.
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
 *
 * The code uses the interface offered by OpenSSL provided with
 * Fedora 29.
 */

#ifndef _OPENSSL_COMMON_H
#define _OPENSSL_COMMON_H

#ifdef __cplusplus
extern "C"
{
#endif

#define _GNU_SOURCE
#include <errno.h>
#include <openssl/aes.h>
#include <openssl/cmac.h>
#include <openssl/crypto.h>
#include <openssl/ecdh.h>
#include <openssl/ecdsa.h>
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/dsa.h>
#include <openssl/dh.h>
#include <openssl/err.h>
#include <openssl/hmac.h>
#include <openssl/kdf.h>
#include <openssl/rand.h>
#include <openssl/rsa.h>
#include <openssl/sha.h>
#include <openssl/modes.h>
#include <stdlib.h>
#include <string.h>

#if OPENSSL_VERSION_NUMBER >= 0x30000000L
#include <openssl/ssl.h>
#include <openssl/core_names.h>
#include <openssl/param_build.h>
#include <openssl/bn.h>
#include <openssl/provider.h>
#endif

#if OPENSSL_VERSION_NUMBER < 0x30000000L
#include <openssl/fips.h>
#endif

#if OPENSSL_VERSION_NUMBER < 0x10100000L
# include <openssl/ssl.h>
#endif

#include "backend_common.h"

#define CKINT_O(x) {							\
	ret = x;							\
	if (ret != 1) {							\
		ret = -EFAULT;						\
		goto out;						\
	}								\
}

#define CKINT_O0(x) {							\
	ret = x;							\
	if (ret == 0) {							\
		ret = -EFAULT;						\
		goto out;						\
	}								\
}

#define CKINT_O_LOG(x, ...) {						\
	ret = x;							\
	if (ret != 1) {							\
		ret = -EFAULT;						\
		logger(LOGGER_ERR,  __VA_ARGS__);			\
		goto out;						\
	}								\
}


/************************************************
 * Configuration of code
 ************************************************/

/*
 * Enable this option to compile the code for the OpenSSL 1.1.x
 * FIPS code base using the upstream CTR DRBG.
 *
 * The default code base works with Fedora 29 / RHEL 8 code base with
 * the add-on CTR / HMAC / Hash DRBG.
 */
#if OPENSSL_VERSION_NUMBER >= 0x30000000L
# define OPENSSL_30X
#endif

#if OPENSSL_VERSION_NUMBER >= 0x10100000L
# ifndef OPENSSL_DRBG_10X
#  define OPENSSL_11X_UPSTREAM_DRBG
# endif
#else
# undef OPENSSL_11X_UPSTREAM_DRBG
#endif

/*
 * Compile the code for OpenSSL 1.0.x
 */
#if OPENSSL_VERSION_NUMBER < 0x10100000L
# define OPENSSL_10X
#endif

/*
 * Enable SHA3 support
 */
#if OPENSSL_VERSION_NUMBER >= 0x10101000L
# define OPENSSL_SSH_SHA3
#endif

/*
 * Enable Keywrap support
 */
#if OPENSSL_VERSION_NUMBER >= 0x10100000L
# define OPENSSL_AESKW
#endif

/*
 * Enable this option if your OpenSSL code base implements the SSH
 * KDF.
 */
#if OPENSSL_VERSION_NUMBER >= 0x10100000L
# define OPENSSL_SSH_KDF
#else
# undef OPENSSL_SSH_KDF
#endif

/*
 * Enable this option if your OpenSSL code base implements the
 * SP800-108 KBKDF.
 */
#ifndef OPENSSL_KBKDF
# define OPENSSL_KBKDF
#endif

/*
 * Enable this option if your OpenSSL code base implements the HKDF.
 */
#if OPENSSL_VERSION_NUMBER >= 0x10100000L
# define OPENSSL_ENABLE_HKDF
#else
# undef OPENSSL_ENABLE_HKDF
#endif

#if OPENSSL_VERSION_NUMBER >= 0x10100000L
# define OPENSSL_ENABLE_TLS13
#else
# undef OPENSSL_ENABLE_TLS13
#endif

int openssl_bn2buf(const BIGNUM *number, struct buffer *buf,
			  uint32_t bufsize);

int openssl_bn2buffer(const BIGNUM *number, struct buffer *buf);

uint32_t be32(uint32_t host);

int openssl_cipher(uint64_t cipher, size_t keylen,
			  const EVP_CIPHER **type);

int openssl_md_convert(uint64_t cipher, const EVP_MD **type);

int openssl_hash_ss(uint64_t cipher, struct buffer *ss,
		struct buffer *hashzz);
int _openssl_ecdsa_curves(uint64_t curve, int *out_nid, char *dgst);

#ifdef OPENSSL_ENABLE_TLS13
int openssl_hkdf_extract(const EVP_MD *md,
			 const uint8_t *key, size_t keylen,
			 const uint8_t *salt, size_t saltlen,
			 uint8_t *secret, size_t *secretlen);
int openssl_hkdf_expand(const EVP_MD *md,
			const uint8_t *fi, size_t filen,
			const uint8_t *secret, size_t secretlen,
			uint8_t *dkm, size_t *dkmlen);
#endif

#ifdef __cplusplus
}
#endif

#endif /* _OPENSSL_COMMON_H */
