/*
 * Copyright (C) 2018 - 2022, Stephan Müller <smueller@chronox.de>
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

#include "backend_openssl_common.h"

ACVP_DEFINE_CONSTRUCTOR(openssl_backend_init)
static void openssl_backend_init(void)
{
	FIPS_mode_set(1);
}

/************************************************
 * OpenSSL version-specific code
 ************************************************/
struct openssl_test_ent {
	struct buffer *entropy;
	struct buffer *nonce;
};

#ifdef OPENSSL_11X_UPSTREAM_DRBG

# include <openssl/rand_drbg.h>

static int idx;

# define DRBG_ctx        		RAND_DRBG
# define DRBG_get_data(a)		RAND_DRBG_get_ex_data(a, idx)
# define DRBG_new(a, b)			RAND_DRBG_new(a, b, NULL)
# define DRBG_set_callbacks(a, b, c)   					\
				RAND_DRBG_set_callbacks(a, b, NULL, c, NULL)
# define DRBG_set_data(a, b)		RAND_DRBG_set_ex_data(a, idx, b)
# define DRBG_instantiate(a, b, c)	RAND_DRBG_instantiate(a, b, c)
# define DRBG_reseed(a, b, c)		RAND_DRBG_reseed(a, b, c, 0)
# define DRBG_generate(a, b, c, d, e, f) RAND_DRBG_generate(a, b, c, d, e, f)
# define DRBG_uninstantiate(a)		RAND_DRBG_uninstantiate(a)
# define DRBG_DF_FLAG			0
# define DRBG_NO_DF_FLAG		RAND_DRBG_FLAG_CTR_NO_DF

static size_t openssl_entropy(RAND_DRBG *dctx, unsigned char **pout,
			      int entropy, size_t min_len, size_t max_len,
			      int prediction_resistance)
{
	struct openssl_test_ent *t = DRBG_get_data(dctx);

	(void) min_len;
	(void) max_len;
	(void) entropy;
	(void) prediction_resistance;

	*pout = (unsigned char *) t->entropy->buf;

	return t->entropy->len;
}

#else

# include <openssl/fips_rand.h>

# define DRBG_ctx			DRBG_CTX
# define DRBG_get_data(a)		FIPS_drbg_get_app_data(a)
# define DRBG_new(a, b)			FIPS_drbg_new(a, b)
# define DRBG_set_callbacks(a, b, c)					\
				FIPS_drbg_set_callbacks(a, b, 0, 0, c, 0)
# define DRBG_set_data(a, b)		FIPS_drbg_set_app_data(a, b)
# define DRBG_instantiate(a, b, c)	FIPS_drbg_instantiate(a, b, c)
# define DRBG_reseed(a, b, c)		FIPS_drbg_reseed(a, b, c)
# define DRBG_generate(a, b, c, d, e, f) FIPS_drbg_generate(a, b, c, d, e, f)
# define DRBG_uninstantiate(a)		FIPS_drbg_uninstantiate(a)
# define DRBG_DF_FLAG			(DRBG_FLAG_CTR_USE_DF | DRBG_FLAG_TEST)
# define DRBG_NO_DF_FLAG		(0 | DRBG_FLAG_TEST)

static size_t openssl_entropy(DRBG_CTX *dctx, unsigned char **pout,
			      int entropy, size_t min_len, size_t max_len)
{
	(void) min_len;
	(void) max_len;
	(void) entropy;
	struct openssl_test_ent *t = DRBG_get_data(dctx);

	*pout = (unsigned char *) t->entropy->buf;

	return t->entropy->len;
}

#endif

#ifdef OPENSSL_10X
int
private_tls1_PRF(long digest_mask,
		 const void *seed1, int seed1_len,
		 const void *seed2, int seed2_len,
		 const void *seed3, int seed3_len,
		 const void *seed4, int seed4_len,
		 const void *seed5, int seed5_len,
		 const unsigned char *sec, int slen,
		 unsigned char *out1,
		 unsigned char *out2,
		 int olen);

# define SSL_HANDSHAKE_MAC_MD5 0x10
# define SSL_HANDSHAKE_MAC_SHA 0x20
# define SSL_HANDSHAKE_MAC_GOST94 0x40
# define SSL_HANDSHAKE_MAC_SHA256 0x80
# define SSL_HANDSHAKE_MAC_SHA384 0x100
# define SSL_HANDSHAKE_MAC_DEFAULT (SSL_HANDSHAKE_MAC_MD5 | SSL_HANDSHAKE_MAC_SHA)

# define TLS1_PRF_DGST_SHIFT 10
# define TLS1_PRF_MD5 (SSL_HANDSHAKE_MAC_MD5 << TLS1_PRF_DGST_SHIFT)
# define TLS1_PRF_SHA1 (SSL_HANDSHAKE_MAC_SHA << TLS1_PRF_DGST_SHIFT)
# define TLS1_PRF_SHA256 (SSL_HANDSHAKE_MAC_SHA256 << TLS1_PRF_DGST_SHIFT)
# define TLS1_PRF_SHA384 (SSL_HANDSHAKE_MAC_SHA384 << TLS1_PRF_DGST_SHIFT)
# define TLS1_PRF_GOST94 (SSL_HANDSHAKE_MAC_GOST94 << TLS1_PRF_DGST_SHIFT)
# define TLS1_PRF (TLS1_PRF_MD5 | TLS1_PRF_SHA1)

#define TLS_MASTER_SECRET_LEN 384/8

static int tls1_PRF(uint64_t cipher,
		    const void *seed1, int seed1_len,
		    const void *seed2, int seed2_len,
		    const void *seed3, int seed3_len,
		    const void *seed4, int seed4_len,
		    const void *seed5, int seed5_len,
		    const unsigned char *sec, int slen,
		    unsigned char *out, int olen)
{
	long digest_mask = 0;
	unsigned char tmp[1024];

	if ((unsigned int)olen > sizeof(tmp)) {
		logger(LOGGER_ERR, "Tmp buffer too small\n");
		return -EINVAL;
	}

	switch (cipher & ACVP_HASHMASK) {
	case ACVP_SHA1:
		digest_mask = TLS1_PRF;
		break;
	case ACVP_SHA256:
		digest_mask = TLS1_PRF_SHA256;
		break;
	case ACVP_SHA384:
		digest_mask = TLS1_PRF_SHA384;
		break;
	default:
		logger(LOGGER_ERR, "Unknown PRF\n");
		return -EINVAL;
	}

	return private_tls1_PRF(digest_mask,
				seed1, seed1_len,
				seed2, seed2_len,
				seed3, seed3_len,
				seed4, seed4_len,
				seed5, seed5_len,
				sec, slen,
				out, tmp, olen);
}

static int openssl_rsa_set0_factors(RSA *r, BIGNUM *p, BIGNUM *q)
{
	r->p = p;
	r->q = q;
	return 1;
}

static int openssl_rsa_set0_key(RSA *r, BIGNUM *n, BIGNUM *e, BIGNUM *d)
{
	r->n = n;
	r->e = e;
	r->d = d;
	return 1;
}

static void openssl_rsa_get0_key(const RSA *r, const BIGNUM **n,
				 const BIGNUM **e, const BIGNUM **d)
{
	*n = r->n;
	*e = r->e;
	*d = r->d;
}
static void openssl_rsa_get0_factors(const RSA *r, const BIGNUM **p,
				     const BIGNUM **q)
{
	*p = r->p;
	*q = r->q;
}

void openssl_dsa_get0_pqg(const DSA *d, const BIGNUM **p,
			  const BIGNUM **q, const BIGNUM **g)
{
	if (p)
		*p = d->p;
	if (q)
		*q = d->q;
	if (g)
		*g = d->g;
}

static int openssl_dsa_set0_pqg(DSA *d, BIGNUM *p, BIGNUM *q, BIGNUM *g)
{
	d->p = p;
	d->q = q;
	d->g = g;
	return 1;
}

static int _openssl_dsa_pqg_gen(struct buffer *P,
				struct buffer *Q,
				struct buffer *G,
				struct buffer *firstseed,
				uint32_t *counter,
				uint32_t L, uint32_t N, uint64_t cipher)
{
	int ret = 0;
	BIGNUM *p = NULL, *q = NULL, *g = NULL;
	DSA *dsa = NULL;
	BN_CTX *ctx = NULL;
	const EVP_MD *md = NULL;
	uint8_t buf[32];
	unsigned long h;

	if ((N >> 3) > sizeof(buf)) {
		logger(LOGGER_ERR, "Insufficient temporary buffer space\n");
		return -EINVAL;
	}

	switch (cipher & (ACVP_HASHMASK | ACVP_HMACMASK | ACVP_SHAKEMASK)) {
	case ACVP_SHA1:
	case ACVP_SHA224:
	case ACVP_SHA256:
		break;
	default:
		logger(LOGGER_ERR, "OpenSSL FIPS_dsa_generate_pq allocates only up to SHA2-256 buffer space - larger hashes are not supported\n");
		return -EINVAL;
	}

	logger(LOGGER_DEBUG, "L = %u\n", L);
	logger(LOGGER_DEBUG, "N = %u\n", N);

	logger(LOGGER_DEBUG, "hash = %" PRIu64 "\n", cipher);
	CKINT(openssl_md_convert(cipher & ACVP_HASHMASK, &md));

	if (firstseed) {
		CKINT(alloc_buf(EVP_MD_size(md), firstseed));

		CKINT_O_LOG(RAND_bytes(firstseed->buf, firstseed->len),
			    "RAND_bytes() failed\n");

		logger_binary(LOGGER_DEBUG, firstseed->buf,
			      firstseed->len, "domain_param_seed");
	}

#if 0
	(void)ctx;

	dsa = DSA_new();
	CKNULL_LOG(dsa, 1, "DSA_new()");

	/*
	 * NOTE: for old OpenSSL-FIPS 2.0.x, replace FIPS_dsa_builtin_paramgen
	 * with dsa_builtin_paramgen.
	 */
	CKINT_O_LOG(FIPS_dsa_builtin_paramgen(dsa, L, N, md,
					      firstseed ? firstseed->buf : NULL,
					      firstseed ? firstseed->len : 0,
					      (int *)counter, &h, NULL),
		    "FIPS_dsa_builtin_paramgen() failed");
	CKINT(openssl_bn2buffer(dsa->p, P));
	CKINT(openssl_bn2buffer(dsa->q, Q));
	if (G)
		CKINT(openssl_bn2buffer(dsa->g, G));
#else
	(void)dsa;

	ctx = BN_CTX_new();
	CKNULL_LOG(ctx, 1, "BN_CTX_new() failed");

	CKINT_O_LOG(FIPS_dsa_generate_pq(ctx, L, N,
					 md, firstseed ? firstseed->buf : buf,
					 firstseed ? firstseed->len : 0,
					 &p, &q,
					 (int *)counter, NULL),
		    "FIPS_dsa_generate_pq() failed");

	CKINT(openssl_bn2buffer(p, P));
	CKINT(openssl_bn2buffer(q, Q));

	if (G) {
		CKINT_O_LOG(FIPS_dsa_generate_g(ctx, p, q, &g, &h, NULL),
						"FIPS_dsa_generate_g() failed");
		CKINT(openssl_bn2buffer(g, G));
	}
#endif

out:
	if (ctx)
		BN_CTX_free(ctx);
	BN_free(p);
	BN_free(q);
	BN_free(g);

	if (dsa)
		DSA_free(dsa);

	return ret;
}

static int openssl_dsa_g_gen(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	BN_CTX *ctx = NULL;
	BIGNUM *p = NULL, *q = NULL, *g = NULL;
	unsigned long h;
	int ret = 0;

	(void)parsed_flags;

	CKINT(left_pad_buf(&data->P, data->L / 8));
	CKINT(left_pad_buf(&data->Q, data->N / 8));

	ctx = BN_CTX_new();
	CKNULL_LOG(ctx, 1, "BN_CTX_new() failed")

	p = BN_bin2bn((const unsigned char *) data->P.buf, data->P.len, p);
	q = BN_bin2bn((const unsigned char *) data->Q.buf, data->Q.len, q);

	CKNULL_LOG(p, 1, "BN_bin2bn() failed");
	CKNULL_LOG(q, 1, "BN_bin2bn() failed");

	CKINT_O_LOG(FIPS_dsa_generate_g(ctx, p, q, &g, &h, NULL),
		    "FIPS_dsa_generate_g() failed");

	CKINT(openssl_bn2buffer(g, &data->G));
	CKNULL_LOG(g, 1, "BN_bn2bin() failed")

out:
	BN_free(p);
	BN_free(q);
	BN_free(g);
	BN_CTX_free(ctx);

	return ret;
}

static int openssl_dsa_pq_ver(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	BIGNUM *p = NULL, *q = NULL, *g = NULL, *rem = NULL;
	BN_CTX *ctx = NULL;
	DSA *dsa = NULL;
	int counter2 = 0;
	unsigned long *h2 = NULL;
	int ret = 0;

	(void)parsed_flags;

	CKINT(left_pad_buf(&data->P, data->L / 8));
	CKINT(left_pad_buf(&data->Q, data->N / 8));
	CKINT(left_pad_buf(&data->domainseed, data->N / 8));

	ctx = BN_CTX_new();
	CKNULL_LOG(ctx, 1, "BN_CTX_new()");

	dsa = DSA_new();
	CKNULL_LOG(dsa, 1, "DSA_new()");

	rem = BN_new();
	CKNULL_LOG(rem, 1, "BN_new()");

	logger_binary(LOGGER_DEBUG, data->P.buf, data->P.len, "P");
	logger_binary(LOGGER_DEBUG, data->Q.buf, data->Q.len, "Q");
	logger_binary(LOGGER_DEBUG, data->G.buf, data->G.len, "G");
	logger_binary(LOGGER_DEBUG, data->domainseed.buf,
		      data->domainseed.len,
		      "Domain parameter seed");
	logger(LOGGER_DEBUG, "Counter = %u\n", data->pq_prob_counter);

	p = BN_bin2bn((const unsigned char *)data->P.buf, data->P.len, NULL);
	CKNULL_LOG(p, -ENOMEM, "BN_bin2bn() failed\n");

	q = BN_bin2bn((const unsigned char *)data->Q.buf, data->Q.len, NULL);
	CKNULL_LOG(q, -ENOMEM, "BN_bin2bn() failed\n");

	if (data->G.len)
		g = BN_bin2bn((const unsigned char *)data->G.buf, data->G.len,
			      NULL);
	else
		g = BN_new();
	CKNULL_LOG(g, -ENOMEM, "BN_bin2bn() failed\n");

	if (1 != BN_is_prime_ex(p, BN_prime_checks, ctx, NULL)) {
		data->pqgver_success = 0;
		logger(LOGGER_DEBUG, "BN_is_prime_ex() failed on p\n");
		goto out;
	}

	if (1 != BN_is_prime_ex(q, BN_prime_checks, ctx, NULL)) {
		data->pqgver_success = 0;
		logger(LOGGER_DEBUG, "BN_is_prime_ex() failed on q\n");
		goto out;
	}

	CKINT_O_LOG(FIPS_dsa_builtin_paramgen(dsa, data->L, data->N, NULL,
					   data->domainseed.buf,
					   data->domainseed.len,
					   &counter2,
					   h2, NULL),
		    "FIPS_dsa_builtin_paramgen() failed\n");

	data->pqgver_success = 1;
	if (BN_cmp(dsa->p, p)) {
		BUFFER_INIT(gen_p_buf);

		CKINT(openssl_bn2buffer(dsa->p, &gen_p_buf));
		logger(LOGGER_DEBUG, "P comparison failed\n");
		logger_binary(LOGGER_DEBUG, gen_p_buf.buf, gen_p_buf.len,
			      "gen P");
		free_buf(&gen_p_buf);
		data->pqgver_success = 0;
	}
	if (BN_cmp(dsa->q, q)) {
		BUFFER_INIT(gen_q_buf);

		CKINT(openssl_bn2buffer(dsa->q, &gen_q_buf));
		logger(LOGGER_DEBUG, "Q comparison failed\n");
		logger_binary(LOGGER_DEBUG, gen_q_buf.buf, gen_q_buf.len,
			      "gen Q");
		free_buf(&gen_q_buf);
		data->pqgver_success = 0;
	}
	if (data->G.len) {
		if (BN_cmp(dsa->g, g)) {
			logger(LOGGER_DEBUG, "G comparison failed\n");
			data->pqgver_success = 0;
		}
	}
	if ((uint32_t)counter2 != data->pq_prob_counter) {
		logger(LOGGER_DEBUG,
		       "Counter mismatch (expected %u, generated %d)\n",
		       data->pq_prob_counter, counter2);
		data->pqgver_success = 0;
	}

out:
	BN_free(p);
	BN_free(q);
	BN_free(g);
	BN_free(rem);
	if (dsa)
		DSA_free(dsa);

	return ret;
}

#if OPENSSL_VERSION_NUMBER >= 0x10002000L
int dsa_paramgen_check_g(DSA *dsa);
#else
/* Not changing the indentation because directly copied from OpenSSL */
static int dsa_paramgen_check_g(DSA *dsa)
{
    BN_CTX *ctx;
    BIGNUM *tmp;
    BN_MONT_CTX *mont = NULL;
    int rv = -1;
    ctx = BN_CTX_new();
    if (!ctx)
        return -1;
    BN_CTX_start(ctx);
    if (BN_cmp(dsa->g, BN_value_one()) <= 0)
        return 0;
    if (BN_cmp(dsa->g, dsa->p) >= 0)
        return 0;
    tmp = BN_CTX_get(ctx);
    if (!tmp)
        goto err;
    if ((mont = BN_MONT_CTX_new()) == NULL)
        goto err;
    if (!BN_MONT_CTX_set(mont, dsa->p, ctx))
        goto err;
    /* Work out g^q mod p */
    if (!BN_mod_exp_mont(tmp, dsa->g, dsa->q, dsa->p, ctx, mont))
        goto err;
    if (!BN_cmp(tmp, BN_value_one()))
        rv = 1;
    else
        rv = 0;
 err:
    BN_CTX_end(ctx);
    if (mont)
        BN_MONT_CTX_free(mont);
    BN_CTX_free(ctx);
    return rv;

}
#endif
static int FIPS_dsa_paramgen_check_g(DSA *dsa)
{
	return dsa_paramgen_check_g(dsa);
}

static void openssl_dsa_get0_key(const DSA *d, const BIGNUM **pub_key,
				 const BIGNUM **priv_key)
{
	*pub_key = d->pub_key;
	*priv_key = d->priv_key;
}

static void openssl_dsa_SIG_get0(const DSA_SIG *sig, const BIGNUM **pr,
				 const BIGNUM **ps)
{
	*pr = sig->r;
	*ps = sig->s;
}

static int openssl_dsa_SIG_set0(DSA_SIG *sig, BIGNUM *r, BIGNUM *s)
{
	sig->r = r;
	sig->s = s;
	return 1;
}

static int openssl_dsa_set0_key(DSA *d, BIGNUM *pub_key, BIGNUM *priv_key)
{
	d->pub_key = pub_key;
	d->priv_key = priv_key;
	return 1;
}

static void openssl_ecdsa_SIG_get0(const ECDSA_SIG *sig, const BIGNUM **pr,
				   const BIGNUM **ps)
{
	*pr = sig->r;
	*ps = sig->s;
}

static int openssl_ecdsa_SIG_set0(ECDSA_SIG *sig, BIGNUM *r, BIGNUM *s)
{
	sig->r = r;
	sig->s = s;
	return 1;
}

static int openssl_dh_set0_pqg(DH *dh, BIGNUM *p, BIGNUM *q, BIGNUM *g)
{
	dh->p = p;
	dh->q = q;
	dh->g = g;
	return 1;
}

static void openssl_dh_get0_key(const DH *dh, const BIGNUM **pub_key,
				const BIGNUM **priv_key)
{
	*pub_key = dh->pub_key;
	*priv_key = dh->priv_key;
}

static int openssl_dh_set0_key(DH *dh, BIGNUM *pub_key, BIGNUM *priv_key)
{
	dh->pub_key = pub_key;
	dh->priv_key =priv_key;
	return 1;
}

#else

/* Copy from ssl/t1_enc.c */
#ifndef OPENSSL_SSH_KDF
static int tls1_PRF(uint64_t cipher,
		    const void *seed1, int seed1_len,
		    const void *seed2, int seed2_len,
		    const void *seed3, int seed3_len,
		    const void *seed4, int seed4_len,
		    const void *seed5, int seed5_len,
		    const unsigned char *sec, int slen,
		    unsigned char *out, int olen)
{
	const EVP_MD *md;
	EVP_PKEY_CTX *pctx = NULL;
	int ret = -EFAULT;
	size_t outlen = olen;

	CKINT(openssl_md_convert(cipher, &md));

	/* Special case */
	if ((cipher & ACVP_HASHMASK) == ACVP_SHA1)
		md = EVP_get_digestbynid(NID_md5_sha1);

	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_TLS1_PRF, NULL);
	if (pctx == NULL || EVP_PKEY_derive_init(pctx) <= 0
		|| EVP_PKEY_CTX_set_tls1_prf_md(pctx, md) <= 0
		|| EVP_PKEY_CTX_set1_tls1_prf_secret(pctx, sec, slen) <= 0)
		goto err;

	if (EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, seed1, seed1_len) <= 0)
		goto err;
	if (EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, seed2, seed2_len) <= 0)
		goto err;
	if (EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, seed3, seed3_len) <= 0)
		goto err;
	if (EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, seed4, seed4_len) <= 0)
		goto err;
	if (EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, seed5, seed5_len) <= 0)
		goto err;

	if (EVP_PKEY_derive(pctx, out, &outlen) <= 0)
		goto err;
	ret = 0;

err:
	EVP_PKEY_CTX_free(pctx);
	return ret;
}
#endif

static int openssl_rsa_set0_factors(RSA *r, BIGNUM *p, BIGNUM *q)
{
	return RSA_set0_factors(r, p, q);
}

static int openssl_rsa_set0_key(RSA *r, BIGNUM *n, BIGNUM *e, BIGNUM *d)
{
	return RSA_set0_key(r, n, e, d);
}

static void openssl_rsa_get0_key(const RSA *r, const BIGNUM **n,
				 const BIGNUM **e, const BIGNUM **d)
{
	RSA_get0_key(r, n, e, d);
}

static void openssl_rsa_get0_factors(const RSA *r, const BIGNUM **p,
				     const BIGNUM **q)
{
	RSA_get0_factors(r, p, q);
}

void openssl_dsa_get0_pqg(const DSA *d, const BIGNUM **p,
			  const BIGNUM **q, const BIGNUM **g)
{
	DSA_get0_pqg(d, p, q, g);
}

static int openssl_dsa_set0_pqg(DSA *d, BIGNUM *p, BIGNUM *q, BIGNUM *g)
{
	return DSA_set0_pqg(d, p, q, g);
}

static int _openssl_dsa_pqg_gen(struct buffer *P,
				struct buffer *Q,
				struct buffer *G,
				struct buffer *firstseed,
				uint32_t *counter,
				uint32_t L, uint32_t N, uint64_t cipher)
{
	DSA *dsa = NULL;
	int ret = 0;
	const EVP_MD *md = NULL;
	const BIGNUM *p, *q, *g;
	unsigned long h;
	unsigned char seed[1024];

	dsa = DSA_new();
	CKNULL_LOG(dsa, -ENOMEM, "DSA_new() failed");

	logger(LOGGER_DEBUG, "L = %u\n", L);
	logger(LOGGER_DEBUG, "N = %u\n", N);

	logger(LOGGER_DEBUG, "hash = %" PRIu64 "\n", cipher);
	CKINT(openssl_md_convert(cipher & ACVP_HASHMASK, &md));

	CKINT_O_LOG(FIPS_dsa_builtin_paramgen2(dsa, L, N, md, NULL, 0,
					       0, seed, (int *)counter,
					       &h, NULL),
		    "FIPS_dsa_builtin_paramgen2() failed %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	openssl_dsa_get0_pqg(dsa, &p, &q, &g);
	CKINT(openssl_bn2buffer(p, P));
	CKINT(openssl_bn2buffer(q, Q));
	CKINT(openssl_bn2buffer(g, G));

	if (firstseed) {
		CKINT(alloc_buf((size_t)EVP_MD_size(md), firstseed));
		memcpy(firstseed->buf, seed, firstseed->len);
	}

	logger_binary(LOGGER_DEBUG, P->buf, P->len, "P");
	logger_binary(LOGGER_DEBUG, Q->buf, Q->len, "Q");
	logger_binary(LOGGER_DEBUG, G->buf, G->len, "G");
	logger(LOGGER_DEBUG, "PQG gen counter: %u\n", *counter);

out:
	if (dsa)
		DSA_free(dsa);

	return ret;
}

static int openssl_dsa_g_gen(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	DSA *dsa = NULL;
	int ret = 0, pqg_consumed = 0;
	const EVP_MD *md = NULL;
	BIGNUM *p = NULL, *q = NULL, *g = NULL;
	const BIGNUM *g_gen;
	unsigned long h;
	int counter;
	unsigned char seed[1024];

	(void)parsed_flags;

	dsa = DSA_new();
	CKNULL_LOG(dsa, -ENOMEM, "DSA_new() failed\n");

	CKINT(left_pad_buf(&data->P, data->L / 8));
	CKINT(left_pad_buf(&data->Q, data->N / 8));

	logger(LOGGER_DEBUG, "L = %u\n", data->L);
	logger(LOGGER_DEBUG, "N = %u\n", data->N);

	logger_binary(LOGGER_DEBUG, data->P.buf, data->P.len, "P");
	logger_binary(LOGGER_DEBUG, data->Q.buf, data->Q.len, "Q");

	p = BN_bin2bn((const unsigned char *)data->P.buf, (int)data->P.len,
		      NULL);
	CKNULL_LOG(p, -ENOMEM, "BN_bin2bn() failed\n");

	q = BN_bin2bn((const unsigned char *)data->Q.buf, (int)data->Q.len,
		      NULL);
	CKNULL_LOG(q, -ENOMEM, "BN_bin2bn() failed\n");

	g = BN_new();
	CKNULL_LOG(g, -ENOMEM, "BN_new() failed\n");

	CKINT_O_LOG(openssl_dsa_set0_pqg(dsa, p, q, g),
		    "DSA_set0_pqg failed\n");
	pqg_consumed = 1;

	logger(LOGGER_DEBUG, "hash = %" PRIu64 "\n", data->cipher);
	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	CKINT_O_LOG(FIPS_dsa_builtin_paramgen2(dsa, data->L, data->N, md,
					       NULL, 0, 0, seed, &counter, &h,
					       NULL),
		    "FIPS_dsa_generate_pq() failed %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	openssl_dsa_get0_pqg(dsa, NULL, NULL, &g_gen);
	CKINT(openssl_bn2buffer(g_gen, &data->G));

	logger_binary(LOGGER_DEBUG, data->G.buf, data->G.len, "G");

	ret = 0;

out:
	if (dsa)
		DSA_free(dsa);
	if (!pqg_consumed && p)
		BN_free(p);
	if (!pqg_consumed && q)
		BN_free(q);
	if (!pqg_consumed && g)
		BN_free(g);

	return ret;
}

static int openssl_dsa_pq_ver(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	DSA *dsa = NULL;
	int ret = 0;
	const EVP_MD *md = NULL;
	BIGNUM *p = NULL, *q = NULL, *g = NULL;
	const BIGNUM *gen_p, *gen_q, *gen_g;
	unsigned long h = 0;
	int counter = 5;
	unsigned char seed[1024];

	(void)parsed_flags;

	dsa = DSA_new();
	CKNULL_LOG(dsa, -ENOMEM, "DSA_new() failed\n");

	CKINT(left_pad_buf(&data->P, data->L / 8));
	CKINT(left_pad_buf(&data->Q, data->N / 8));
	CKINT(left_pad_buf(&data->domainseed, data->N / 8));

	logger(LOGGER_DEBUG, "L = %u\n", data->L);
	logger(LOGGER_DEBUG, "N = %u\n", data->N);

	logger_binary(LOGGER_DEBUG, data->P.buf, data->P.len, "P");
	logger_binary(LOGGER_DEBUG, data->Q.buf, data->Q.len, "Q");
	logger_binary(LOGGER_DEBUG, data->domainseed.buf,
		      data->domainseed.len,
		      "Domain parameter seed");
	logger(LOGGER_DEBUG, "Counter = %u\n", data->pq_prob_counter);

	p = BN_bin2bn((const unsigned char *)data->P.buf, (int)data->P.len,
		      NULL);
	CKNULL_LOG(p, -ENOMEM, "BN_bin2bn() failed\n");

	q = BN_bin2bn((const unsigned char *)data->Q.buf, (int)data->Q.len,
		      NULL);
	CKNULL_LOG(q, -ENOMEM, "BN_bin2bn() failed\n");

	if (data->G.len)
		g = BN_bin2bn((const unsigned char *)data->G.buf,
			      (int)data->G.len, NULL);
	else
		g = BN_new();
	CKNULL_LOG(g, -ENOMEM, "BN_bin2bn() failed\n");

	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	ret = FIPS_dsa_builtin_paramgen2(dsa, data->L, data->N, md,
					 data->domainseed.buf,
					 data->domainseed.len,
					 (int)data->pq_prob_counter,
				 	 seed, &counter, &h, NULL);
	if (ret < 0) {
		ret = -EFAULT;
		logger(LOGGER_ERR, "FIPS_dsa_builtin_paramgen2() failed\n");
		goto out;
	} else if (ret == 0) {
		ret = 1;
		data->pqgver_success = 0;
		goto out;
	} else {
		ret = 0;
		data->pqgver_success = 1;
	}

	openssl_dsa_get0_pqg(dsa, &gen_p, &gen_q, &gen_g);

	if (BN_cmp(gen_p, p)) {
		BUFFER_INIT(gen_p_buf);

		CKINT(openssl_bn2buffer(gen_p, &gen_p_buf));
		logger(LOGGER_DEBUG, "P comparison failed\n");
		logger_binary(LOGGER_DEBUG, gen_p_buf.buf, gen_p_buf.len,
			      "gen P");
		free_buf(&gen_p_buf);
		data->pqgver_success = 0;
	}
	if (BN_cmp(gen_q, q)) {
		BUFFER_INIT(gen_q_buf);

		CKINT(openssl_bn2buffer(gen_q, &gen_q_buf));
		logger(LOGGER_DEBUG, "Q comparison failed\n");
		logger_binary(LOGGER_DEBUG, gen_q_buf.buf, gen_q_buf.len,
			      "gen Q");
		free_buf(&gen_q_buf);
		data->pqgver_success = 0;
	}
	if (data->G.len) {
		if (BN_cmp(gen_g, g)) {
			logger(LOGGER_DEBUG, "G comparison failed\n");
			data->pqgver_success = 0;
		}
	}
	if ((uint32_t)counter != data->pq_prob_counter) {
		logger(LOGGER_DEBUG,
		       "Counter mismatch (expected %u, generated %d)\n",
		       data->pq_prob_counter, counter);
		data->pqgver_success = 0;
	}

	ret = 0;

out:
	if (dsa)
		DSA_free(dsa);
	if (p)
		BN_free(p);
	if (q)
		BN_free(q);
	if (g)
		BN_free(g);

	return ret;
}

static void openssl_dsa_get0_key(const DSA *d, const BIGNUM **pub_key,
				 const BIGNUM **priv_key)
{
	DSA_get0_key(d, pub_key, priv_key);
}

static void openssl_dsa_SIG_get0(const DSA_SIG *sig, const BIGNUM **pr,
				 const BIGNUM **ps)
{
	DSA_SIG_get0(sig, pr, ps);
}

static int openssl_dsa_SIG_set0(DSA_SIG *sig, BIGNUM *r, BIGNUM *s)
{
	return DSA_SIG_set0(sig, r, s);
}

static int openssl_dsa_set0_key(DSA *d, BIGNUM *pub_key, BIGNUM *priv_key)
{
	return DSA_set0_key(d, pub_key, priv_key);
}

static void openssl_ecdsa_SIG_get0(const ECDSA_SIG *sig, const BIGNUM **pr,
				   const BIGNUM **ps)
{
	ECDSA_SIG_get0(sig, pr, ps);
}

static int openssl_ecdsa_SIG_set0(ECDSA_SIG *sig, BIGNUM *r, BIGNUM *s)
{
	return ECDSA_SIG_set0(sig, r, s);
}

static int openssl_dh_set0_pqg(DH *dh, BIGNUM *p, BIGNUM *q, BIGNUM *g)
{
	return DH_set0_pqg(dh, p, q, g);
}

static void openssl_dh_get0_key(const DH *dh, const BIGNUM **pub_key,
				const BIGNUM **priv_key)
{
	DH_get0_key(dh, pub_key, priv_key);
}

static int openssl_dh_set0_key(DH *dh, BIGNUM *pub_key, BIGNUM *priv_key)
{
	return DH_set0_key(dh, pub_key, priv_key);
}
#endif

/************************************************
 * CMAC/HMAC cipher interface functions
 ************************************************/
static int openssl_cmac_generate(struct hmac_data *data)
{
	const EVP_CIPHER *type = NULL;
	CMAC_CTX *ctx = NULL;
	int blocklen;
	int ret = 0;

	ctx = CMAC_CTX_new();
	CKNULL(ctx, -ENOMEM);

	CKINT(openssl_cipher(data->cipher, data->key.len, &type));

	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");

	CKINT_O_LOG(CMAC_Init(ctx, data->key.buf, data->key.len, type, NULL),
		    "CMAC_Init() failed\n");

	blocklen = EVP_CIPHER_block_size(type);
	CKINT_LOG(alloc_buf((size_t)blocklen, &data->mac),
		  "CMAC buffer cannot be allocated\n");

	logger(LOGGER_DEBUG, "tag length = %d", blocklen);

	CKINT_O_LOG(CMAC_Update(ctx, data->msg.buf, data->msg.len),
		    "CMAC_Update() failed\n");

	CKINT_O_LOG(CMAC_Final(ctx, data->mac.buf, (size_t *) &data->mac.len),
		    "CMAC_Final() failed\n");

	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "mac");

	// Truncate to desired macLen, which is in bits
	if (data->mac.len > data->maclen / 8) {
		data->mac.buf[data->maclen / 8] = '\0';
		data->mac.len = data->maclen / 8;
		logger(LOGGER_DEBUG, "Truncated mac to maclen: %d\n", data->maclen);
		logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "mac");
	}

	ret = 0;

out:
	if (ctx)
		CMAC_CTX_free(ctx);

	return ret;
}

static int openssl_hmac_generate(struct hmac_data *data)
{
	const EVP_MD *md = NULL;
	unsigned char hmac[EVP_MAX_MD_SIZE];
	unsigned int taglen;
	int mdlen;
	int ret = 0;

	CKINT(openssl_md_convert(data->cipher, &md));

	mdlen = EVP_MD_size(md);

	CKINT_LOG(alloc_buf((size_t)mdlen, &data->mac),
		  "SHA buffer cannot be allocated\n");

	taglen = (unsigned int)data->mac.len;

	logger(LOGGER_DEBUG, "taglen = %zu\n", data->mac.len);
	logger_binary(LOGGER_DEBUG, data->key.buf, data->key.len, "key");
	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");

	if (!HMAC(md, data->key.buf, (int)data->key.len,
		 data->msg.buf, (unsigned int)data->msg.len,
		 hmac, &taglen)) {
		logger(LOGGER_WARN, "HMAC failed: %s\n",
		       ERR_error_string(ERR_get_error(), NULL));
		ret = -EINVAL;
		goto out;
	}

	memcpy(data->mac.buf, hmac, data->mac.len);
	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "hmac");

out:
	return ret;
}

static int openssl_mac_generate(struct hmac_data *data, flags_t parsed_flags)
{
	(void)parsed_flags;

	switch(data->cipher) {
	case ACVP_AESCMAC:
	case ACVP_TDESCMAC:
		return openssl_cmac_generate(data);
		break;
	default:
		return openssl_hmac_generate(data);
		break;
	}

	return -EFAULT;
}

static struct hmac_backend openssl_mac =
{
	openssl_mac_generate,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_mac_backend)
static void openssl_mac_backend(void)
{
	register_hmac_impl(&openssl_mac);
}

/************************************************
 * DRBG cipher interface functions
 ************************************************/
static size_t openssl_nonce(DRBG_ctx *dctx, unsigned char **pout,
			    int entropy, size_t min_len, size_t max_len)
{
	(void) min_len;
	(void) max_len;
	(void) entropy;
	struct openssl_test_ent *t = DRBG_get_data(dctx);

	*pout = (unsigned char * )t->nonce->buf;

	return t->nonce->len;
}

static int openssl_drbg_generate(struct drbg_data *data, flags_t parsed_flags)
{
	DRBG_ctx *ctx = NULL;
	unsigned int df = 0;
	int nid = NID_undef, ret = 0;
	struct openssl_test_ent t;

	(void)parsed_flags;

	logger(LOGGER_DEBUG, "cipher: %" PRIu64 "\n", data->cipher);

	if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA1) {
		nid = ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				NID_hmacWithSHA1 : NID_sha1;
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA224) {
		nid = ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				NID_hmacWithSHA224 : NID_sha224;
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA256) {
		nid = ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				NID_hmacWithSHA256 : NID_sha256;
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA384) {
		nid = ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				NID_hmacWithSHA384 : NID_sha384;
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA512) {
		nid = ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC) ?
				NID_hmacWithSHA512 : NID_sha512;
	} else if ((data->cipher & ACVP_AESMASK) == ACVP_AES128) {
		nid = NID_aes_128_ctr;
	} else if ((data->cipher & ACVP_AESMASK) == ACVP_AES192) {
		nid = NID_aes_192_ctr;
	} else if ((data->cipher & ACVP_AESMASK) == ACVP_AES256) {
		nid = NID_aes_256_ctr;
	} else {
		logger(LOGGER_WARN, "DRBG with unhandled cipher detected\n");
		return -EFAULT;
	}

	if (data->df)
		df = DRBG_DF_FLAG;
	else
		df = DRBG_NO_DF_FLAG;

	ctx = DRBG_new(nid, df);
	CKNULL(ctx, -ENOMEM);

	logger_binary(LOGGER_DEBUG, data->entropy.buf, data->entropy.len,
		      "entropy");
	t.entropy = &data->entropy;

	logger_binary(LOGGER_DEBUG, data->nonce.buf, data->nonce.len, "nonce");
	t.nonce = &data->nonce;
	
	DRBG_set_callbacks(ctx, openssl_entropy, openssl_nonce);
	DRBG_set_data(ctx, &t);

	logger_binary(LOGGER_DEBUG, data->pers.buf, data->pers.len,
		      "personalization string");

	CKINT_O_LOG(DRBG_instantiate(ctx, data->pers.buf, data->pers.len),
		    "DRBG instantiation failed: %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	if (data->entropy_reseed.buffers[0].len) {
		logger_binary(LOGGER_DEBUG,
			      data->entropy_reseed.buffers[0].buf,
			      data->entropy_reseed.buffers[0].len,
			      "entropy reseed");
		t.entropy = &data->entropy_reseed.buffers[0];

		if (data->addtl_reseed.buffers[0].len) {
			logger_binary(LOGGER_DEBUG,
				      data->addtl_reseed.buffers[0].buf,
				      data->addtl_reseed.buffers[0].len,
				      "addtl reseed");
		}
		CKINT_O(DRBG_reseed(ctx, data->addtl_reseed.buffers[0].buf,
				    data->addtl_reseed.buffers[0].len));
	}

	if (data->pr) {
		logger_binary(LOGGER_DEBUG,
			      data->entropy_generate.buffers[0].buf,
			      data->entropy_generate.buffers[0].len,
			      "entropy generate 1");
		t.entropy = &data->entropy_generate.buffers[0];
	}

	logger_binary(LOGGER_DEBUG, data->addtl_generate.buffers[0].buf,
		      data->addtl_generate.buffers[0].len, "addtl generate 1");

	CKINT(alloc_buf(data->rnd_data_bits_len / 8, &data->random));

	CKINT_O_LOG(DRBG_generate(ctx, data->random.buf, data->random.len,
				  data->entropy_generate.buffers[0].len?1:0,
				  data->addtl_generate.buffers[0].buf,
				  data->addtl_generate.buffers[0].len),
		    "FIPS_drbg_generate failed\n");

	logger_binary(LOGGER_DEBUG, data->random.buf, data->random.len,
		      "random tmp");

	if (data->pr) {
		logger_binary(LOGGER_DEBUG,
			      data->entropy_generate.buffers[1].buf,
			      data->entropy_generate.buffers[1].len,
			      "entropy generate 2");
		t.entropy = &data->entropy_generate.buffers[1];
	}

	logger_binary(LOGGER_DEBUG, data->addtl_generate.buffers[1].buf,
		      data->addtl_generate.buffers[1].len, "addtl generate 2");

	CKINT_O_LOG(DRBG_generate(ctx, data->random.buf, data->random.len,
				  data->entropy_generate.buffers[1].len?1:0,
				  data->addtl_generate.buffers[1].buf,
				  data->addtl_generate.buffers[1].len),
		    "FIPS_drbg_generate failed\n");

	logger_binary(LOGGER_DEBUG, data->random.buf, data->random.len,
		      "random");

	ret = 0;

out:
	if (ctx)
		DRBG_uninstantiate(ctx);

	return ret;
}

static struct drbg_backend openssl_drbg =
{
	openssl_drbg_generate,  /* drbg_generate */
};

ACVP_DEFINE_CONSTRUCTOR(openssl_drbg_backend)
static void openssl_drbg_backend(void)
{
	register_drbg_impl(&openssl_drbg);
}

#ifdef OPENSSL_SSH_KDF
#include <openssl/ssl.h>
#include <openssl/kdf.h>
/************************************************
 * TLS cipher interface functions
 ************************************************/

static int openssl_kdf_tls_op(struct kdf_tls_data *data, flags_t parsed_flags)
{
	EVP_PKEY_CTX *pctx = NULL;
	const EVP_MD *md;
	int ret;

	(void)parsed_flags;

	CKINT(openssl_md_convert(data->hashalg, &md));

	/* Special case */
	if ((data->hashalg & ACVP_HASHMASK) == ACVP_SHA1)
		md = EVP_get_digestbynid(NID_md5_sha1);

	CKNULL_LOG(md, -EFAULT, "Cipher implementation not found\n");

	CKINT(alloc_buf(data->pre_master_secret.len, &data->master_secret));

	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_TLS1_PRF, NULL);
	CKNULL_LOG(pctx, -EFAULT, "Cannot allocate TLS1 PRF\n");

	CKINT_O(EVP_PKEY_derive_init(pctx));
	CKINT_O(EVP_PKEY_CTX_set_tls1_prf_md(pctx, md));
	CKINT_O(EVP_PKEY_CTX_set1_tls1_prf_secret(pctx,
						  data->pre_master_secret.buf,
						  data->pre_master_secret.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
					TLS_MD_MASTER_SECRET_CONST,
					TLS_MD_MASTER_SECRET_CONST_SIZE));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->client_hello_random.buf,
						data->client_hello_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->server_hello_random.buf,
						data->server_hello_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_derive(pctx, data->master_secret.buf,
				&data->master_secret.len));

	logger_binary(LOGGER_DEBUG, data->master_secret.buf,
		      data->master_secret.len, "master_secret");

	EVP_PKEY_CTX_free(pctx);
	pctx = NULL;

	CKINT(alloc_buf(data->key_block_length / 8, &data->key_block));

	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_TLS1_PRF, NULL);
	CKNULL_LOG(pctx, -EFAULT, "Cannot allocate TLS1 PRF\n");

	CKINT_O(EVP_PKEY_derive_init(pctx));
	CKINT_O(EVP_PKEY_CTX_set_tls1_prf_md(pctx, md));
	CKINT_O(EVP_PKEY_CTX_set1_tls1_prf_secret(pctx,
						  data->master_secret.buf,
						  data->master_secret.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
					TLS_MD_KEY_EXPANSION_CONST,
					TLS_MD_KEY_EXPANSION_CONST_SIZE));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->server_random.buf,
						data->server_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->client_random.buf,
						data->client_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_derive(pctx, data->key_block.buf,
				&data->key_block.len));

	logger_binary(LOGGER_DEBUG, data->key_block.buf, data->key_block.len,
		      "keyblock");

	ret = 0;

out:
	EVP_PKEY_CTX_free(pctx);
	return (ret);
}

static struct kdf_tls_backend openssl_kdf_tls =
{
	openssl_kdf_tls_op,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_kdf_tls_backend)
static void openssl_kdf_tls_backend(void)
{
	register_kdf_tls_impl(&openssl_kdf_tls);
}


static int openssl_tls12_op(struct tls12_data *data, flags_t parsed_flags)
{
	EVP_PKEY_CTX *pctx = NULL;
	const EVP_MD *md;
	int ret;

	(void)parsed_flags;

	CKINT(openssl_md_convert(data->hashalg, &md));

	/* Special case */
	if ((data->hashalg & ACVP_HASHMASK) == ACVP_SHA1)
		md = EVP_get_digestbynid(NID_md5_sha1);

	CKNULL_LOG(md, -EFAULT, "Cipher implementation not found\n");

	CKINT(alloc_buf(data->pre_master_secret.len, &data->master_secret));

	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_TLS1_PRF, NULL);
	CKNULL_LOG(pctx, -EFAULT, "Cannot allocate TLS1 PRF\n");

	CKINT_O(EVP_PKEY_derive_init(pctx));
	CKINT_O(EVP_PKEY_CTX_set_tls1_prf_md(pctx, md));
	CKINT_O(EVP_PKEY_CTX_set1_tls1_prf_secret(pctx,
						  data->pre_master_secret.buf,
						  data->pre_master_secret.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
				TLS_MD_EXTENDED_MASTER_SECRET_CONST,
				TLS_MD_EXTENDED_MASTER_SECRET_CONST_SIZE));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->session_hash.buf,
						data->session_hash.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_derive(pctx, data->master_secret.buf,
				&data->master_secret.len));

	logger_binary(LOGGER_DEBUG, data->master_secret.buf,
		      data->master_secret.len, "master_secret");

	EVP_PKEY_CTX_free(pctx);
	pctx = NULL;

	CKINT(alloc_buf(data->key_block_length / 8, &data->key_block));

	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_TLS1_PRF, NULL);
	CKNULL_LOG(pctx, -EFAULT, "Cannot allocate TLS1 PRF\n");

	CKINT_O(EVP_PKEY_derive_init(pctx));
	CKINT_O(EVP_PKEY_CTX_set_tls1_prf_md(pctx, md));
	CKINT_O(EVP_PKEY_CTX_set1_tls1_prf_secret(pctx,
						  data->master_secret.buf,
						  data->master_secret.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
					TLS_MD_KEY_EXPANSION_CONST,
					TLS_MD_KEY_EXPANSION_CONST_SIZE));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->server_random.buf,
						data->server_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx,
						data->client_random.buf,
						data->client_random.len));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_CTX_add1_tls1_prf_seed(pctx, NULL, 0));
	CKINT_O(EVP_PKEY_derive(pctx, data->key_block.buf,
				&data->key_block.len));

	logger_binary(LOGGER_DEBUG, data->key_block.buf, data->key_block.len,
		      "keyblock");

	ret = 0;

out:
	EVP_PKEY_CTX_free(pctx);
	return (ret);
}

static struct tls12_backend openssl_tls12 =
{
	openssl_tls12_op,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_tls12_backend)
static void openssl_tls12_backend(void)
{
	register_tls12_impl(&openssl_tls12);
}

/************************************************
 * SSHv2 KDF
 ************************************************/
#ifdef UBUNTU
# define	EVP_KDF_CTX		EVP_PKEY_CTX
# define 	EVP_KDF_CTX_NEW_ID()	EVP_PKEY_CTX_new_id(EVP_PKEY_SSHKDF,NULL)
# define	EVP_KDF_DERIVE_INIT(a)	EVP_PKEY_derive_init(a)
# define	EVP_KDF_SET_MD(a,b)	EVP_PKEY_CTX_set_sshkdf_md(a,b)
# define	EVP_KDF_SET_KEY(a,b,c)	EVP_PKEY_CTX_set1_sshkdf_key(a,b,c)
# define	EVP_KDF_SET_XCGHASH(a,b,c)				\
					EVP_PKEY_CTX_set1_sshkdf_xcghash(a,b,c)
# define	EVP_KDF_SET_SESSIONID(a,b,c)				\
					EVP_PKEY_CTX_set1_sshkdf_session_id(a,b,c)
# define	EVP_KDF_SET_SSHKDF_TYPE(a,b)				\
					EVP_PKEY_CTX_set_sshkdf_type(a,b)
# define	EVP_KDF_DERIVE(a,b,c)	EVP_PKEY_derive(a,b,&c)
# define	EVP_KDF_CTX_FREE(a)	EVP_PKEY_CTX_free(a)
#else
# define	EVP_KDF_CTX_NEW_ID()	EVP_KDF_CTX_new_id(EVP_KDF_SSHKDF)
# define	EVP_KDF_DERIVE_INIT(a)	1
# define	EVP_KDF_SET_MD(a,b)	EVP_KDF_ctrl(a,EVP_KDF_CTRL_SET_MD,b)
# define	EVP_KDF_SET_KEY(a,b,c)	EVP_KDF_ctrl(a,EVP_KDF_CTRL_SET_KEY,b,c)
# define	EVP_KDF_SET_XCGHASH(a,b,c)				\
			EVP_KDF_ctrl(a,EVP_KDF_CTRL_SET_SSHKDF_XCGHASH,b,c)
# define	EVP_KDF_SET_SESSIONID(a,b,c)				\
			EVP_KDF_ctrl(a,EVP_KDF_CTRL_SET_SSHKDF_SESSION_ID,b,c)
# define	EVP_KDF_SET_SSHKDF_TYPE(a,b)				\
			EVP_KDF_ctrl(a,EVP_KDF_CTRL_SET_SSHKDF_TYPE,b)
# define	EVP_KDF_DERIVE(a,b,c)	EVP_KDF_derive(a,b,c)
# define	EVP_KDF_CTX_FREE(a)	EVP_KDF_CTX_free(a)
#endif

static int openssl_kdf_ssh_internal(struct kdf_ssh_data *data,
				    int id, const EVP_MD *md,
				    struct buffer *out)
{
	EVP_KDF_CTX *ctx = NULL;
	int ret = 0;

	ctx = EVP_KDF_CTX_NEW_ID();
	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate SSHv2 PRF\n");

	CKINT_O(EVP_KDF_DERIVE_INIT(ctx));
	CKINT_O(EVP_KDF_SET_MD(ctx, md));
	CKINT_O(EVP_KDF_SET_KEY(ctx, data->k.buf, data->k.len));
	CKINT_O(EVP_KDF_SET_XCGHASH(ctx, data->h.buf, data->h.len));
	CKINT_O(EVP_KDF_SET_SSHKDF_TYPE(ctx, id));
	CKINT_O(EVP_KDF_SET_SESSIONID(ctx, data->session_id.buf,
				      data->session_id.len));
	CKINT_O(EVP_KDF_DERIVE(ctx, out->buf, out->len));

out:
	EVP_KDF_CTX_FREE(ctx);
	return ret;
}

static int openssl_kdf_ssh(struct kdf_ssh_data *data, flags_t parsed_flags)
{
	const EVP_MD *md;
	unsigned int ivlen, enclen, maclen;
	int ret;

	(void)parsed_flags;

	CKINT(openssl_md_convert(data->cipher, &md));

	switch (data->cipher & ACVP_SYMMASK) {
	case ACVP_AES128:
		enclen = 16;
		ivlen = 16;
		break;
	case ACVP_AES192:
		enclen = 24;
		ivlen = 16;
		break;
	case ACVP_AES256:
		enclen = 32;
		ivlen = 16;
		break;
	case ACVP_TDESECB:
		enclen = 24;
		ivlen = 8;
		break;
	default:
		logger(LOGGER_WARN, "Cipher not identified\n");
		ret = -EINVAL;
		goto out;
	}

	switch (data->cipher & ACVP_HASHMASK) {
	case ACVP_SHA1:
		maclen = 20;
		break;
	case ACVP_SHA256:
		maclen = 32;
		break;
	case ACVP_SHA384:
		maclen = 48;
		break;
	case ACVP_SHA512:
		maclen = 64;
		break;
	default:
		logger(LOGGER_WARN, "Mac not identified\n");
		ret = -EINVAL;
		goto out;
	}

	CKINT(alloc_buf(ivlen, &data->initial_iv_client));
	CKINT(alloc_buf(ivlen, &data->initial_iv_server));
	CKINT(alloc_buf(enclen, &data->encryption_key_client));
	CKINT(alloc_buf(enclen, &data->encryption_key_server));
	CKINT(alloc_buf(maclen, &data->integrity_key_client));
	CKINT(alloc_buf(maclen, &data->integrity_key_server));

	CKINT(openssl_kdf_ssh_internal(data,  'A' + 0, md,
				       &data->initial_iv_client));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 1, md,
				       &data->initial_iv_server));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 2, md,
				       &data->encryption_key_client));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 3, md,
				       &data->encryption_key_server));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 4, md,
				       &data->integrity_key_client));
	CKINT(openssl_kdf_ssh_internal(data,  'A' + 5, md,
				       &data->integrity_key_server));

out:
	return ret;
}

static struct kdf_ssh_backend openssl_kdf =
{
	openssl_kdf_ssh,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_kdf_ssh_backend)
static void openssl_kdf_ssh_backend(void)
{
	register_kdf_ssh_impl(&openssl_kdf);
}

#else /* OPENSSL_SSH_KDF */

/************************************************
 * TLS cipher interface functions
 ************************************************/

static int openssl_kdf_tls_op(struct kdf_tls_data *data, flags_t parsed_flags)
{
	int ret;

	(void)parsed_flags;

	SSL_library_init();
	SSL_load_error_strings();

	CKINT(alloc_buf(data->pre_master_secret.len, &data->master_secret));

	CKINT_O_LOG(tls1_PRF(data->hashalg,
			     TLS_MD_MASTER_SECRET_CONST,
			     TLS_MD_MASTER_SECRET_CONST_SIZE,
			     data->client_hello_random.buf,
			     data->client_hello_random.len, NULL, 0,
			     data->server_hello_random.buf,
			     data->server_hello_random.len, NULL, 0,
			     data->pre_master_secret.buf,
			     data->pre_master_secret.len,
			     data->master_secret.buf,
			     data->master_secret.len),
		  "Generation of master secret failed\n");

	logger_binary(LOGGER_DEBUG, data->master_secret.buf,
		      data->master_secret.len, "master_secret");

	CKINT(alloc_buf(data->key_block_length / 8, &data->key_block));
	CKINT_O_LOG(tls1_PRF(data->hashalg,
			     TLS_MD_KEY_EXPANSION_CONST,
			     TLS_MD_KEY_EXPANSION_CONST_SIZE,
			     data->server_random.buf, data->server_random.len,
			     data->client_random.buf, data->client_random.len,
			     NULL, 0, NULL, 0,
			     data->master_secret.buf, data->master_secret.len,
			     data->key_block.buf, data->key_block.len),
		  "Generation of key block failed\n");

	logger_binary(LOGGER_DEBUG, data->key_block.buf, data->key_block.len,
		      "keyblock");

	ret = 0;

out:
	return (ret);
}

static struct kdf_tls_backend openssl_kdf_tls =
{
	openssl_kdf_tls_op,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_kdf_tls_backend)
static void openssl_kdf_tls_backend(void)
{
	register_kdf_tls_impl(&openssl_kdf_tls);
}
#endif /* OPENSSL_SSH_KDF */

#ifdef OPENSSL_KBKDF
/************************************************
 * SP 800-108 KBKDF interface functions
 ************************************************/

static int openssl_kdf108(struct kdf_108_data *data, flags_t parsed_flags)
{
	EVP_KDF_CTX *ctx = NULL;
	const EVP_MD *md = NULL;
	const EVP_CIPHER *type = NULL;
	uint32_t derived_key_bytes = data->derived_key_length / 8;
	uint32_t l = be32(data->derived_key_length);
	BUFFER_INIT(label);
	BUFFER_INIT(context);
	int ret = 0, alloced = 0;
	(void)parsed_flags;

	logger(LOGGER_VERBOSE, "data->kdfmode = %" PRIu64 "\n", data->kdfmode);
	if (!(data->kdfmode & ACVP_CIPHERTYPE_KDF)) {
		logger(LOGGER_ERR, "The cipher type isn't a KDF");
		ret = -EINVAL;
		goto out;
	}

	if (data->kdfmode == ACVP_KDF_108_DOUBLE_PIPELINE) {
		logger(LOGGER_ERR, "Double pipeline mode is not supported");
		ret = -EINVAL;
		goto out;
	}

	ctx = EVP_KDF_CTX_new_id(EVP_KDF_KB);
	CKNULL(ctx, -ENOMEM);

	/* We only check COUNTER or FEEDBACK because DOUBLE PIPELINE is not
	 * supported and is checked above
	 */
	CKINT_O_LOG(EVP_KDF_ctrl(ctx, EVP_KDF_CTRL_SET_KB_MODE,
				(data->kdfmode == ACVP_KDF_108_COUNTER) ?
				 EVP_KDF_KB_MODE_COUNTER :
				 EVP_KDF_KB_MODE_FEEDBACK),
		    "EVP_KDF_ctrl failed to set KB_MODE");

	logger(LOGGER_VERBOSE, "data->mac = %" PRIu64 "\n", data->mac);
	if (data->mac & ACVP_CIPHERTYPE_HMAC) {
		CKINT(openssl_md_convert(data->mac, &md));
		CKNULL(md, -ENOMEM);

		CKINT_O_LOG(EVP_KDF_ctrl(ctx, EVP_KDF_CTRL_SET_MD, md),
			    "EVP_KDF_ctrl failed to set the MD\n");
		CKINT_O_LOG(EVP_KDF_ctrl(ctx, EVP_KDF_CTRL_SET_KB_MAC_TYPE,
					 EVP_KDF_KB_MAC_TYPE_HMAC),
			    "EVP_KDF_ctrl failed to set the MAC_TYPE\n");
	} else if (data->mac & ACVP_CIPHERTYPE_CMAC) {
		CKINT(openssl_cipher(data->mac == ACVP_AESCMAC ? ACVP_AESCMAC :
				     ACVP_TDESCMAC, data->key.len, &type));
		CKNULL(type, -ENOMEM);

		CKINT_O_LOG(EVP_KDF_ctrl(ctx, EVP_KDF_CTRL_SET_CIPHER, type),
			    "EVP_KDF_ctrl failed to set the CIPHER\n");
		CKINT_O_LOG(EVP_KDF_ctrl(ctx, EVP_KDF_CTRL_SET_KB_MAC_TYPE,
					 EVP_KDF_KB_MAC_TYPE_CMAC),
                            "EVP_KDF_ctrl failed to set the MAC_TYPE\n");
	}

	logger_binary(LOGGER_VERBOSE, data->key.buf, data->key.len, "data->key");
	CKINT_O_LOG(EVP_KDF_ctrl(ctx, EVP_KDF_CTRL_SET_KEY,
				 data->key.buf, data->key.len),
		    "EVP_KDF_ctrl failed to set the KEY");

	logger(LOGGER_VERBOSE, "L = %u\n", derived_key_bytes);
	logger_binary(LOGGER_VERBOSE, (unsigned char *)&l, sizeof(l), "[L]_2");

	if (data->fixed_data.len) {
		if (data->fixed_data.len != (data->key.len * 2 + 1 + sizeof(l))) {
			logger(LOGGER_ERR, "KBKDF fixed data unexpected length for regression testing\n");
			ret = -EINVAL;
			goto out;
		}
		label.buf = data->fixed_data.buf;
		label.len = data->key.len;
		context.buf = data->fixed_data.buf + 1 + label.len;
		context.len = data->key.len;
	} else {
		alloced = 1;
		CKINT(alloc_buf(data->key.len, &label));
		CKINT(alloc_buf(data->key.len, &context));

		/*
		 * Allocate the fixed_data to hold
		 * Label || 0x00 || Context || [L]_2
		 */
		CKINT(alloc_buf(label.len + 1 + context.len + sizeof(l),
				&data->fixed_data));

		/* Randomly choose the label and context */
		RAND_bytes(label.buf, (int)label.len);
		RAND_bytes(context.buf, (int)context.len);

		/*
		 * Fixed data = Label || 0x00 || Context || [L]_2
		 * The counter i is not part of it
		 */
		memcpy(data->fixed_data.buf, label.buf, label.len);
		       data->fixed_data.buf[label.len] = 0x00;
		memcpy(data->fixed_data.buf + label.len + 1, context.buf,
		       context.len);
		memcpy(data->fixed_data.buf + label.len + 1 + context.len,
		       (unsigned char *)&l, sizeof(l));

		logger_binary(LOGGER_VERBOSE, data->fixed_data.buf,
			      data->fixed_data.len, "data->fixed_data");
	}

	logger_binary(LOGGER_VERBOSE, label.buf, label.len, "label");
	CKINT_O_LOG(EVP_KDF_ctrl(ctx, EVP_KDF_CTRL_SET_SALT, label.buf,
				label.len),
		    "EVP_KDF_ctrl failed to set the SALT (label)");

	logger_binary(LOGGER_VERBOSE, context.buf, context.len, "context");
	CKINT_O_LOG(EVP_KDF_ctrl(ctx, EVP_KDF_CTRL_SET_KB_INFO, context.buf,
				context.len),
		    "EVP_KDF_ctrl fail to set KB_INFO (context)");

	if (data->iv.len) {
		logger_binary(LOGGER_VERBOSE, data->iv.buf, data->iv.len,
			      "data->iv");
		CKINT_O_LOG(EVP_KDF_ctrl(ctx, EVP_KDF_CTRL_SET_KB_SEED,
					 data->iv.buf, data->iv.len),
			    "EVP_KDF_ctrl failed to set the KB_SEED (iv)");
	}

	CKINT(alloc_buf(derived_key_bytes, &data->derived_key));
	CKINT_O_LOG(EVP_KDF_DERIVE(ctx, data->derived_key.buf,
				   derived_key_bytes),
		    "EVP_KDF_DERIVE failed\n");
	logger_binary(LOGGER_VERBOSE, data->derived_key.buf,
                      derived_key_bytes, "data->derived_key");

out:
	EVP_KDF_CTX_free(ctx);
	if (alloced) {
		free_buf(&label);
		free_buf(&context);
	}
	return ret;
}

static struct kdf_108_backend openssl_kdf108_backend =
{
	openssl_kdf108,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_kdf_108_backend)
static void openssl_kdf_108_backend(void)
{
	register_kdf_108_impl(&openssl_kdf108_backend);
}
#endif

/************************************************
 * RSA interface functions
 ************************************************/

static int openssl_rsa_keygen_prime(struct rsa_keygen_prime_data *data,
				    flags_t parsed_flags)
{
	BIGNUM *e = NULL, *p = NULL, *q = NULL;
	RSA *rsa = NULL;
	int ret = 0;

	(void)parsed_flags;

	if (!data->e.len) {
		logger(LOGGER_WARN, "RSA E missing\n");
		return -EINVAL;
	}

	rsa = RSA_new();
	CKNULL(rsa, -ENOMEM);

	logger_binary(LOGGER_DEBUG, data->e.buf, data->e.len, "e");
	logger_binary(LOGGER_DEBUG, data->p.buf, data->p.len, "p");
	logger_binary(LOGGER_DEBUG, data->q.buf, data->q.len, "q");

	e = BN_bin2bn((const unsigned char *) data->e.buf, (int)data->e.len, e);
	CKNULL(e, -ENOMEM);

	p = BN_bin2bn((const unsigned char *) data->p.buf, (int)data->p.len, p);
	CKNULL(p, -ENOMEM);
	if (BN_is_zero(p))
		BN_one(p);

	q = BN_bin2bn((const unsigned char *)data->q.buf, (int)data->q.len, q);
	CKNULL(q, -ENOMEM);
	if (BN_is_zero(q))
		BN_one(q);

	CKINT_O_LOG(openssl_rsa_set0_factors(rsa, p, q), "P/Q cannot be set\n");

	ret = RSA_generate_key_ex(rsa, (int)data->modulus, e, NULL);
	if (ret == 1) {
		logger(LOGGER_DEBUG, "RSA_generate_key_ex passed for RSA\n");
		data->keygen_success = 1;
		ret = 0;
	} else if (ret == 0) {
		logger(LOGGER_DEBUG, "RSA_generate_key_ex failed for RSA\n");
		data->keygen_success = 0;
	} else {
		logger(LOGGER_DEBUG,
		       "RSA_generate_key_ex general error for RSA\n");
		ret = -EFAULT;
	}

out:
	if (e)
		BN_free(e);
	if (rsa)
		RSA_free(rsa);

	return ret;
}

static int openssl_rsa_keygen_internal(struct buffer *ebuf, uint32_t modulus,
				       RSA **outkey, struct buffer *nbuf,
				       struct buffer *dbuf, struct buffer *pbuf,
				       struct buffer *qbuf)
{
	BIGNUM *e = NULL;
	const BIGNUM *egen, *n, *d, *p, *q;
	RSA *rsa = NULL;
	unsigned int retry = 0;
	int ret = 0;

	if (!ebuf->len) {
		unsigned int a;
		uint8_t bitsset = 0;

		/* WARNING Buffer must be at least 3 bytes in size ! */
		CKINT(alloc_buf(sizeof(unsigned int), ebuf));

		/* generate random odd e */
		RAND_bytes(ebuf->buf, (int)ebuf->len);
		/* make sure it is odd */
		ebuf->buf[ebuf->len - 1] |= 1;

		for (a = 0; a < ebuf->len - 2; a++)
			bitsset |= ebuf->buf[a];

		/* Make sure that value is >= 65537 */
		if (!bitsset)
			ebuf->buf[ebuf->len - 3] |= 1;
	}

	logger(LOGGER_DEBUG, "modulus: %u\n", modulus);
	logger_binary(LOGGER_DEBUG, ebuf->buf, ebuf->len, "e");

#if 1
	e = BN_bin2bn((const unsigned char *)ebuf->buf, (int)ebuf->len, e);
	CKNULL(e, -ENOMEM);
#else
	e = BN_new();
	CKNULL(e, -ENOMEM);
	if (1 != BN_set_word(e, 65537)) {
		logger(LOGGER_WARN, "BN_set_word() failed");
		ret = -EFAULT;
		goto out;
	}
#endif

	do {
		if (rsa)
			RSA_free(rsa);
		rsa = RSA_new();
		CKNULL(rsa, -ENOMEM);

		ret = RSA_generate_key_ex(rsa, (int)modulus, e, NULL);
		retry++;
	} while (ret != 1 && retry < 100);
	CKINT_O_LOG(ret, "RSA_generate_key_ex() failed: %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	openssl_rsa_get0_key(rsa, &n, &egen, &d);
	openssl_rsa_get0_factors(rsa, &p, &q);

	free_buf(ebuf);
	CKINT(openssl_bn2buffer(egen, ebuf));

	if (nbuf)
		CKINT(openssl_bn2buffer(n, nbuf));
	if (dbuf)
		CKINT(openssl_bn2buffer(d, dbuf));
	if (pbuf)
		CKINT(openssl_bn2buffer(p, pbuf));
	if (qbuf)
		CKINT(openssl_bn2buffer(q, qbuf));

	if (outkey) {
		*outkey = rsa;
		rsa = NULL;
	}

	ret = 0;

out:
	if (e)
		BN_free(e);
	if (rsa)
		RSA_free(rsa);

	return ret;
}

static int openssl_rsa_keygen(struct rsa_keygen_data *data,
			      flags_t parsed_flags)
{
	(void)parsed_flags;

	return openssl_rsa_keygen_internal(&data->e, data->modulus, NULL,
					   &data->n, &data->d, &data->p,
					   &data->q);
}

static int openssl_rsa_keygen_en(struct buffer *ebuf, uint32_t modulus,
				 void **privkey, struct buffer *nbuf)
{
	return openssl_rsa_keygen_internal(ebuf, modulus, (RSA **)privkey, nbuf,
					   NULL, NULL, NULL);
}

static void openssl_rsa_free_key(void *privkey)
{
	RSA *rsa = (RSA *)privkey;

	if (rsa)
		RSA_free(rsa);
}

static int openssl_rsa_siggen(struct rsa_siggen_data *data,
			      flags_t parsed_flags)
{
	const EVP_MD *md = NULL;
	EVP_MD_CTX *ctx = NULL;
	EVP_PKEY_CTX *pctx = NULL;
	EVP_PKEY *pk = NULL;
	RSA *rsa = NULL;
	size_t siglen;
	int ret;

	(void)parsed_flags;

	if (!data->privkey) {
		logger(LOGGER_ERR, "Private key missing\n");
		return -EINVAL;
	}

	rsa = data->privkey;

	CKINT(openssl_md_convert(data->cipher, &md));

	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");

	pk = EVP_PKEY_new();
	CKNULL(pk, -ENOMEM);

	EVP_PKEY_set1_RSA(pk, rsa);

	CKINT(alloc_buf((size_t)EVP_PKEY_size(pk), &data->sig));
	siglen = data->sig.len;

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -ENOMEM);

	CKINT_O_LOG(EVP_DigestSignInit(ctx, &pctx, md, NULL, pk),
		    "EVP_DigestSignInit failed: %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	if (parsed_flags & FLAG_OP_RSA_SIG_PKCS1PSS) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_PKCS1_PSS_PADDING),
			    "Setting PSS type failed: %s\n", ERR_error_string(ERR_get_error(), NULL));
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_pss_saltlen(pctx,
						data->saltlen),
			    "Setting salt length to %u failed: %s\n",
			    data->saltlen,
			    ERR_error_string(ERR_get_error(), NULL));
	}

	if (parsed_flags & FLAG_OP_RSA_SIG_X931) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_X931_PADDING),
			    "Setting X9.31 type failed: %s\n", ERR_error_string(ERR_get_error(), NULL));
	}

	CKINT_O_LOG(EVP_DigestSignUpdate(ctx, data->msg.buf, data->msg.len),
		    "EVP_DigestSignUpdate failed: %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	CKINT_O_LOG(EVP_DigestSignFinal(ctx, data->sig.buf, &siglen),
		    "EVP_DigestSignFinal failed: %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	logger_binary(LOGGER_DEBUG, data->sig.buf, data->sig.len, "sig");

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);
	if (pk)
		EVP_PKEY_free(pk);

	return ret;
}

static int openssl_rsa_sigver(struct rsa_sigver_data *data,
			      flags_t parsed_flags)
{
	const EVP_MD *md = NULL;
	EVP_MD_CTX *ctx = NULL;
	EVP_PKEY_CTX *pctx = NULL;
	EVP_PKEY *pk = NULL;
	RSA *rsa = NULL;
	BIGNUM *n = NULL, *e = NULL;
	int ret = 0;

	(void)parsed_flags;

	if (!data->n.len || !data->e.len) {
		logger(LOGGER_WARN, "RSA N or E missing\n");
		return -EINVAL;
	}

	CKINT(left_pad_buf(&data->n, data->modulus / 8));
	CKINT(left_pad_buf(&data->sig, data->modulus / 8));

	n = BN_bin2bn((const unsigned char *)data->n.buf, (int)data->n.len, n);
	CKNULL(n, -ENOMEM);
	e = BN_bin2bn((const unsigned char *)data->e.buf, (int)data->e.len, e);
	CKNULL(e, -ENOMEM);

	CKINT(openssl_md_convert(data->cipher, &md));

	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");

	rsa = RSA_new();
	CKNULL(rsa, -ENOMEM);

	CKINT_O_LOG(openssl_rsa_set0_key(rsa, n, e, NULL),
		    "Assembly of RSA key failed\n");

	pk = EVP_PKEY_new();
	CKNULL(pk, -ENOMEM);

	EVP_PKEY_set1_RSA(pk, rsa);

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -ENOMEM);

	CKINT_O(EVP_DigestVerifyInit(ctx, &pctx, md, NULL, pk));

	if (parsed_flags & FLAG_OP_RSA_SIG_PKCS1PSS) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_PKCS1_PSS_PADDING),
			    "Setting PSS type failed: %s\n",
			    ERR_error_string(ERR_get_error(), NULL));
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_pss_saltlen(pctx,
						data->saltlen),
			    "Setting salt length to %u failed: %s\n",
			    data->saltlen,
			    ERR_error_string(ERR_get_error(), NULL));
	}

	if (parsed_flags & FLAG_OP_RSA_SIG_X931) {
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(pctx,
						RSA_X931_PADDING),
			    "Setting X9.31 type failed: %s\n",
			    ERR_error_string(ERR_get_error(), NULL));
	}

        CKINT_O(EVP_DigestVerifyUpdate(ctx, data->msg.buf, data->msg.len));

	ret = EVP_DigestVerifyFinal(ctx, data->sig.buf, data->sig.len);
	if (!ret) {
		logger(LOGGER_DEBUG, "Signature verification: signature bad\n");
		data->sig_result = 0;
	} else if (ret == 1) {
		logger(LOGGER_DEBUG,
		       "Signature verification: signature good\n");
		data->sig_result = 1;
		ret = 0;
	} else {
		logger(LOGGER_WARN,
		       "Signature verification: general error\n");
		ret = -EFAULT;
	}

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);
	if (rsa)
		RSA_free(rsa);
	if (pk)
		EVP_PKEY_free(pk);
	/* n and e do not need to be freed as they belong to the RSA context. */

	return ret;
}

static int
openssl_rsa_decryption_primitive(struct rsa_decryption_primitive_data *data,
				 flags_t parsed_flags)
{
	EVP_PKEY_CTX *ctx = NULL;
	size_t outlen;
	EVP_PKEY *key = NULL;
	RSA *rsa = NULL;
	int ret;

	(void)parsed_flags;

	rsa = data->privkey;
	CKNULL_LOG(rsa, -EFAULT, "RSA key missing\n");

	key = EVP_PKEY_new();
	CKNULL(key, -ENOMEM);
	EVP_PKEY_set1_RSA(key, rsa);

	ctx = EVP_PKEY_CTX_new(key, NULL);
	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate PKEY context\n");


	CKINT_O_LOG(EVP_PKEY_decrypt_init(ctx), "PKEY decrypt init failed\n");

	CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_NO_PADDING),
		    "Disabling padding failed\n")

	/* Determine buffer length */
	CKINT_O_LOG(EVP_PKEY_decrypt(ctx, NULL, &outlen, data->msg.buf,
				     data->msg.len),
		    "Getting plaintext length failed\n");

	CKINT(alloc_buf(outlen, &data->s));

	ret = EVP_PKEY_decrypt(ctx, data->s.buf, &outlen, data->msg.buf,
			       data->msg.len);
	if (ret == 1) {
		logger(LOGGER_DEBUG, "Decryption successful\n");
		data->dec_result = 1;
	} else {
		logger(LOGGER_DEBUG, "Decryption failed %s\n",
		       ERR_error_string(ERR_get_error(), NULL));
		data->dec_result = 0;
	}

	ret = 0;

out:
	if (key)
		EVP_PKEY_free(key);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static struct rsa_backend openssl_rsa =
{
	openssl_rsa_keygen,     /* rsa_keygen */
	openssl_rsa_siggen,     /* rsa_siggen */
	openssl_rsa_sigver,     /* rsa_sigver */
	openssl_rsa_keygen_prime,              /* rsa_keygen_prime */
	NULL,		        /* rsa_keygen_prov_prime */
	openssl_rsa_keygen_en,
	openssl_rsa_free_key,
	NULL,
	openssl_rsa_decryption_primitive,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_rsa_backend)
static void openssl_rsa_backend(void)
{
	register_rsa_impl(&openssl_rsa);
}

/************************************************
 * DSA interface functions
 ************************************************/

static int openssl_dsa_pqggen(struct dsa_pqggen_data *data,
			      flags_t parsed_flags)
{
	DSA *dsa = NULL;
	uint32_t counter;
	int ret;

	(void)parsed_flags;
	CKINT(_openssl_dsa_pqg_gen(&data->P, &data->Q, &data->G, NULL,
				   &counter, data->L, data->N, data->cipher));

out:
	if (dsa)
		DSA_free(dsa);

	return ret;
}

static int openssl_dsa_pq_gen(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	(void)parsed_flags;
	return _openssl_dsa_pqg_gen(&data->P, &data->Q, &data->G,
				    &data->domainseed,
				    &data->pq_prob_counter,
				    data->L, data->N, data->cipher);
}

static int openssl_dsa_pqg_ver(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	DSA *dsa = NULL;
	int ret = 0, pqg_consumed = 0;
	BIGNUM *p = NULL, *q = NULL, *g = NULL;

	(void)parsed_flags;

	dsa = DSA_new();
	CKNULL_LOG(dsa, -ENOMEM, "DSA_new() failed\n");

	CKINT(left_pad_buf(&data->P, data->L / 8));
	CKINT(left_pad_buf(&data->Q, data->N / 8));
	CKINT(left_pad_buf(&data->G, data->L / 8));

	logger(LOGGER_DEBUG, "L = %u\n", data->L);
	logger(LOGGER_DEBUG, "N = %u\n", data->N);

	logger_binary(LOGGER_DEBUG, data->P.buf, data->P.len, "P");
	logger_binary(LOGGER_DEBUG, data->Q.buf, data->Q.len, "Q");
	logger_binary(LOGGER_DEBUG, data->G.buf, data->G.len, "G");

	p = BN_bin2bn((const unsigned char *)data->P.buf, (int)data->P.len,
		      NULL);
	CKNULL_LOG(p, -ENOMEM, "BN_bin2bn() failed\n");

	q = BN_bin2bn((const unsigned char *)data->Q.buf, (int)data->Q.len,
		      NULL);
	CKNULL_LOG(q, -ENOMEM, "BN_bin2bn() failed\n");

	g = BN_bin2bn((const unsigned char *)data->G.buf, (int)data->G.len,
		      NULL);
	CKNULL_LOG(g, -ENOMEM, "BN_bin2bn() failed\n");

	CKINT_O_LOG(openssl_dsa_set0_pqg(dsa, p, q, g),
		    "DSA_set0_pqg failed\n");
	pqg_consumed = 1;

	if (1 == FIPS_dsa_paramgen_check_g(dsa)) {
		data->pqgver_success = 1;
		logger(LOGGER_DEBUG, "PQG verification successful\n");
	} else {
		data->pqgver_success = 0;
		logger(LOGGER_DEBUG, "PQG verification failed\n");
	}

	ret = 0;

out:
	if (dsa)
		DSA_free(dsa);
	if (!pqg_consumed && p)
		BN_free(p);
	if (!pqg_consumed && q)
		BN_free(q);
	if (!pqg_consumed && g)
		BN_free(g);

	return ret;
}

static int openssl_dsa_pqg(struct dsa_pqg_data *data, flags_t parsed_flags)
{
	parsed_flags &= ~FLAG_OP_GDT;
	if (parsed_flags ==
	    (FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_PROBABLE_PQ_GEN))
		return openssl_dsa_pq_gen(data, parsed_flags);
	else if (parsed_flags ==
		 (FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_PROBABLE_PQ_GEN))
		return openssl_dsa_pq_ver(data, parsed_flags);
	else if (parsed_flags ==
		 (FLAG_OP_DSA_TYPE_PQGGEN | FLAG_OP_DSA_UNVERIFIABLE_G_GEN))
		return openssl_dsa_g_gen(data, parsed_flags);
	else if (parsed_flags ==
		 (FLAG_OP_DSA_TYPE_PQGVER | FLAG_OP_DSA_UNVERIFIABLE_G_GEN))
		return openssl_dsa_pqg_ver(data, parsed_flags);
	else {
		logger(LOGGER_WARN,
		       "Unknown DSA PQG generation / verification definition (parsed flags: %" PRIu64 ")\n",
		       parsed_flags);
		return -EINVAL;
	}
}

#if 0
static int _openssl_dsa_pqg_gen_public_api(struct buffer *P,
					   struct buffer *Q,
					   struct buffer *G,
					   uint32_t L)
{
	DSA *dsa = NULL;
	int ret = 0;
	const BIGNUM *p, *q, *g;

	dsa = DSA_new();
	CKNULL_LOG(dsa, -ENOMEM, "DSA_new() failed\n");

	logger(LOGGER_DEBUG, "L = %u\n", L);

	/* If L >= 2048, OpenSSL applies N = 256, SHA-256 */
	if (1 != DSA_generate_parameters_ex(dsa, L, NULL, 0, NULL, NULL,
					    NULL)) {
		logger(LOGGER_WARN, "DSA_generate_parameters_ex() failed\n");
		ret = - EFAULT;
		goto out;
	}

	DSA_get0_pqg(dsa, &p, &q, &g);
	CKINT(openssl_bn2buffer(p, P));
	CKINT(openssl_bn2buffer(q, Q));
	CKINT(openssl_bn2buffer(g, G));

	//logger_binary(LOGGER_DEBUG, P->buf, P->len, "P");
	//logger_binary(LOGGER_DEBUG, Q->buf, Q->len, "Q");
	//logger_binary(LOGGER_DEBUG, G->buf, G->len, "G");

out:
	if (dsa)
		DSA_free(dsa);

	return ret;
}
#endif

static int openssl_dh_set_param(const struct buffer *P /* [in] */,
			        const struct buffer *Q /* [in] */,
			        const struct buffer *G /* [in] */,
			        uint64_t safeprime /* [in] */,
				DH *dh /* [out] */,
				size_t *keylen /* [out] */)
{
	BIGNUM *p = NULL, *q = NULL, *g = NULL;
	int ret = 0, pqg_consumed = 0;

	/*
	 * TODO change to
	 * BIGNUM *BN_get_rfc3526_prime_2048(BIGNUM *bn);
	 * BIGNUM *BN_get_rfc3526_prime_3072(BIGNUM *bn);
	 * BIGNUM *BN_get_rfc3526_prime_4096(BIGNUM *bn);
	 * BIGNUM *BN_get_rfc3526_prime_6144(BIGNUM *bn);
	 * BIGNUM *BN_get_rfc3526_prime_8192(BIGNUM *bn);
	 */
	if (P && P->len && Q && Q->len && G && G->len) {
		p = BN_bin2bn((const unsigned char *)P->buf, (int)P->len, NULL);
		CKNULL_LOG(p, -ENOMEM, "BN_bin2bn() failed\n");

		q = BN_bin2bn((const unsigned char *)Q->buf, (int)Q->len, NULL);
		CKNULL_LOG(q, -ENOMEM, "BN_bin2bn() failed\n");

		g = BN_bin2bn((const unsigned char *)G->buf, (int)G->len, NULL);
		CKNULL_LOG(g, -ENOMEM, "BN_bin2bn() failed\n");
		if (keylen)
			*keylen = P->len;
	} else {
		struct safeprimes *p_safeprime;

		CKINT(acvp_safeprime_get(safeprime, &p_safeprime));

		CKINT_O0(BN_hex2bn(&p, p_safeprime->p));
		CKINT_O0(BN_hex2bn(&q, p_safeprime->q));
		CKINT_O0(BN_hex2bn(&g, p_safeprime->g));

		if (keylen)
			*keylen = p_safeprime->p_b.len;
	}

	CKINT_O_LOG(openssl_dh_set0_pqg(dh, p, q, g),
		    "DSA_set0_pqg failed\n");
	pqg_consumed = 1;

	ret = 0;

out:
	if (!pqg_consumed && p)
		BN_free(p);
	if (!pqg_consumed && q)
		BN_free(q);
	if (!pqg_consumed && g)
		BN_free(g);

	return ret;
}

static int _openssl_dh_keygen(struct buffer *P /* [in] */,
			      struct buffer *Q /* [in] */,
			      struct buffer *G /* [in] */,
			      uint64_t safeprime /* [in] */,
			      struct buffer *X /* [out] */,
			      struct buffer *Y /* [out] */)
{
	DH *dh = NULL;
	const BIGNUM *x, *y;
	int ret = 0;

	dh = DH_new();
	CKNULL_LOG(dh, -ENOMEM, "DH_new() failed\n");

	CKINT(openssl_dh_set_param(P, Q, G, safeprime, dh, NULL));

	CKINT_O_LOG(DH_generate_key(dh), "DH_generate_key() failed\n");

	openssl_dh_get0_key(dh, &y, &x);

	CKINT(openssl_bn2buffer(x, X));
	CKINT(openssl_bn2buffer(y, Y));

	//logger_binary(LOGGER_DEBUG, X->buf, X->len, "X");
	//logger_binary(LOGGER_DEBUG, Y->buf, Y->len, "Y");

	ret = 0;

out:
	if (dh)
		DH_free(dh);

	return ret;
}

static int _openssl_dsa_keygen(struct buffer *P /* [in] */,
			       struct buffer *Q /* [in] */,
			       struct buffer *G /* [in] */,
			       uint64_t safeprime /* [in] */,
			       struct buffer *X /* [out] */,
			       struct buffer *Y /* [out] */,
			       DSA **dsa)
{
	BIGNUM *p = NULL, *q = NULL, *g = NULL;
	const BIGNUM *x, *y;
	int ret = 0, pqg_consumed = 0;

	switch (safeprime) {
	case ACVP_DH_MODP_2048:
	case ACVP_DH_MODP_3072:
	case ACVP_DH_MODP_4096:
	case ACVP_DH_MODP_6144:
	case ACVP_DH_MODP_8192:
		logger(LOGGER_WARN, "Automatically using Safeprime testing with DH operation - safeprime testing with DSA interface not supported (Q not set\n");
		return _openssl_dh_keygen(P, Q, G, safeprime, X, Y);
	default:
		p = BN_bin2bn((const unsigned char *)P->buf, (int)P->len, NULL);
		CKNULL_LOG(p, -ENOMEM, "BN_bin2bn() failed\n");

		q = BN_bin2bn((const unsigned char *)Q->buf, (int)Q->len, NULL);
		CKNULL_LOG(q, -ENOMEM, "BN_bin2bn() failed\n");

		g = BN_bin2bn((const unsigned char *)G->buf, (int)G->len, NULL);
		CKNULL_LOG(g, -ENOMEM, "BN_bin2bn() failed\n");
	}

	*dsa = DSA_new();
	CKNULL_LOG(*dsa, -ENOMEM, "DSA_new() failed\n");

	CKINT_O_LOG(openssl_dsa_set0_pqg(*dsa, p, q, g),
		    "DSA_set0_pqg failed\n");
	pqg_consumed = 1;

	CKINT_O_LOG(DSA_generate_key(*dsa), "DSA_generate_key() failed\n");

	openssl_dsa_get0_key(*dsa, &y, &x);

	CKINT(openssl_bn2buffer(x, X));
	CKINT(openssl_bn2buffer(y, Y));

	//logger_binary(LOGGER_DEBUG, X->buf, X->len, "X");
	//logger_binary(LOGGER_DEBUG, Y->buf, Y->len, "Y");

	ret = 0;

out:
	if (!pqg_consumed && p)
		BN_free(p);
	if (!pqg_consumed && q)
		BN_free(q);
	if (!pqg_consumed && g)
		BN_free(g);

	return ret;
}

static int openssl_dsa_keygen(struct dsa_keygen_data *data,
			      flags_t parsed_flags)
{
	struct dsa_pqggen_data *pqg = &data->pqg;
	DSA *dsa = NULL;
	int ret;
	char *envstr = NULL;

	(void)parsed_flags;

	envstr = secure_getenv("OPENSSL_ACVP_DH_KEYGEN");

	if (envstr) {
		CKINT(_openssl_dh_keygen(&pqg->P, &pqg->Q, &pqg->G,
					 pqg->safeprime,
					 &data->X, &data->Y));
	} else {
		CKINT(_openssl_dsa_keygen(&pqg->P, &pqg->Q, &pqg->G,
					  pqg->safeprime,
					  &data->X, &data->Y, &dsa));
	}

out:
	if (dsa)
		DSA_free(dsa);

	return ret;
}

static int openssl_dh_keygen(struct dh_keygen_data *data,
			      flags_t parsed_flags)
{
	int ret = 0;
	(void)parsed_flags;

	CKINT(_openssl_dh_keygen(NULL, NULL, NULL, data->safeprime,
				 &data->X, &data->Y));
out:
	return ret;
}

static int _openssl_dh_keyver(const struct buffer *P, const struct buffer *Q,
			      const struct buffer *G,
			      const uint64_t safeprime,
			      const struct buffer *X, const struct buffer *Y,
			      uint32_t *keyver_success)
{
	DH *dh = NULL;
	BIGNUM *y = NULL, *x = NULL;
	const BIGNUM *nx, *ny;
	int ret = 0, key_consumed = 0;

	dh = DH_new();
	CKNULL_LOG(dh, -ENOMEM, "DH_new() failed\n");

	CKINT(openssl_dh_set_param(P, Q, G, safeprime, dh,
				   NULL));

	y = BN_bin2bn((const unsigned char *) Y->buf, (int)Y->len, y);
	CKNULL(y, -ENOMEM);
	x = BN_bin2bn((const unsigned char *) X->buf, (int)X->len, x);
	CKNULL(x, -ENOMEM);

	/*
	 * NOTE: the following tests are expected to be performed:
	 * Invalid key pair, x must satisfy 0 < x < q
	 * Invalid key pair, y != g^x mod p
	 *
	 * This is NOT implemented in OpenSSL, but can be achieved with the
	 * following code.
	 */

	/* Check that the provided public key truly matches the private key */
	CKINT(openssl_dh_set0_key(dh, NULL, x));
	key_consumed = 1;
	CKINT_O_LOG(DH_generate_key(dh), "DH_generate_key failed\n");
	openssl_dh_get0_key(dh, &ny, &nx);

	if (BN_cmp(ny, y) != 0) {
		*keyver_success = 0;
		logger(LOGGER_DEBUG,
		       "Key verification failed: provided Y and calculated Y inconsistent\n");
		ret = 0;
		goto out;
	}

#if 0
	/* Check appropriateness of public key */
	int check_code = 0;
	CKINT_O_LOG(DH_check_pub_key(dh, y, &check_code),
		    "DH_check_pub_key failed\n");
	if (check_code != 0) {
		data->keyver_success = 0;
		logger(LOGGER_DEBUG,
		       "Key verification failed with error code %d\n",
		       check_code);
		ret = 0;
		goto out;
	}
#endif

	*keyver_success = 1;
	logger(LOGGER_DEBUG, "Key verification successful\n");

	ret = 0;

out:
	if (y)
		BN_free(y);
	if (!key_consumed && x)
		BN_free(x);
	if (dh)
		DH_free(dh);

	return ret;
}

static int openssl_dsa_keyver(struct dsa_keyver_data *data,
			     flags_t parsed_flags)
{
	int reset = 0, ret;

	(void)parsed_flags;

	if (data->pqg.P.len && data->pqg.Q.len && data->pqg.G.len) {
		FIPS_mode_set(0);
		reset = 1;
	}

	ret = _openssl_dh_keyver(&data->pqg.P, &data->pqg.Q, &data->pqg.G,
				 data->pqg.safeprime, &data->X, &data->Y,
				 &data->keyver_success);

	if (reset)
		FIPS_mode_set(1);

	return ret;
}


static int openssl_dh_keyver(struct dh_keyver_data *data,
			     flags_t parsed_flags)
{
	(void)parsed_flags;
	return _openssl_dh_keyver(NULL, NULL, NULL,
				  data->safeprime, &data->X, &data->Y,
				  &data->keyver_success);
}


static int openssl_dsa_sigver(struct dsa_sigver_data *data,
			      flags_t parsed_flags)
{
	struct dsa_pqggen_data *pqg = &data->pqg;
	EVP_MD_CTX *ctx = NULL;
	const EVP_MD *md = NULL;
	EVP_PKEY *pk = NULL;
	DSA *dsa = NULL;
	DSA_SIG *sig = NULL;
	BIGNUM *p = NULL, *q = NULL, *g = NULL, *y = NULL, *r = NULL, *s = NULL;
	unsigned int sig_len;
	int ret = 0, key_consumed = 0, pqg_consumed = 0, sig_consumed = 0;
	unsigned char sig_buf[1024];
	unsigned char *sig_buf_p = sig_buf;

	(void)parsed_flags;

	dsa = DSA_new();
	CKNULL_LOG(dsa, -ENOMEM, "DSA_new() failed\n");

	sig = DSA_SIG_new();
	CKNULL_LOG(sig, -ENOMEM, "DSA_SIG_new() failed\n");

	CKINT(left_pad_buf(&pqg->P, pqg->L / 8));
	CKINT(left_pad_buf(&pqg->Q, pqg->N / 8));
	CKINT(left_pad_buf(&pqg->G, pqg->L / 8));
	CKINT(left_pad_buf(&data->Y, pqg->L / 8));
	CKINT(left_pad_buf(&data->R, pqg->N / 8));
	CKINT(left_pad_buf(&data->S, pqg->N / 8));

	p = BN_bin2bn((const unsigned char *) pqg->P.buf, (int)pqg->P.len, p);
	CKNULL(p, -ENOMEM);
	q = BN_bin2bn((const unsigned char *) pqg->Q.buf, (int)pqg->Q.len, q);
	CKNULL(q, -ENOMEM);
	g = BN_bin2bn((const unsigned char *) pqg->G.buf, (int)pqg->G.len, g);
	CKNULL(g, -ENOMEM);
	y = BN_bin2bn((const unsigned char *) data->Y.buf, (int)data->Y.len, y);
	CKNULL(y, -ENOMEM);
	r = BN_bin2bn((const unsigned char *) data->R.buf, (int)data->R.len, r);
	CKNULL(r, -ENOMEM);
	s = BN_bin2bn((const unsigned char *) data->S.buf, (int)data->S.len, s);
	CKNULL(s, -ENOMEM);

	CKINT_O_LOG(openssl_dsa_set0_pqg(dsa, p, q, g),
		    "DSA_set0_pqg failed\n");
	pqg_consumed = 1;

	CKINT_O_LOG(openssl_dsa_set0_key(dsa, y, NULL),
		    "DSA_set0_key failed\n");
	key_consumed = 1;

	CKINT_O_LOG(openssl_dsa_SIG_set0(sig, r, s), "DSA_SIG_set0 failed\n");
	sig_consumed = 1;

	logger_binary(LOGGER_DEBUG, pqg->P.buf, pqg->P.len, "P");
	logger_binary(LOGGER_DEBUG, pqg->Q.buf, pqg->Q.len, "Q");
	logger_binary(LOGGER_DEBUG, pqg->G.buf, pqg->G.len, "G");
	logger_binary(LOGGER_DEBUG, data->Y.buf, data->Y.len, "Y");
	logger_binary(LOGGER_DEBUG, data->R.buf, data->R.len, "R");
	logger_binary(LOGGER_DEBUG, data->S.buf, data->S.len, "S");
	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");

	logger(LOGGER_DEBUG, "cipher = %" PRIu64 "\n", data->cipher);

	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	pk = EVP_PKEY_new();
	CKNULL(pk, -ENOMEM);

	EVP_PKEY_set1_DSA(pk, dsa);
	sig_len = (unsigned int)i2d_DSA_SIG(sig, &sig_buf_p);

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -ENOMEM);

	if (!EVP_VerifyInit_ex(ctx, md, NULL)) {
		ret = -EFAULT;
		goto out;
	}

	if (!EVP_VerifyUpdate(ctx, data->msg.buf, data->msg.len)) {
		ret = -EFAULT;
		goto out;
	}

	ret = EVP_VerifyFinal(ctx, sig_buf, sig_len, pk);
	if (!ret) {
		logger(LOGGER_DEBUG, "Signature verification: signature bad\n");
		data->sigver_success = 0;
	} else if (ret == 1) {
		logger(LOGGER_DEBUG,
		       "Signature verification: signature good\n");
		data->sigver_success = 1;
		ret = 0;
	} else {
		logger(LOGGER_WARN,
		       "Signature verification: general error\n");
		ret = -EFAULT;
	}

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);
	if (sig)
		DSA_SIG_free(sig);
	if (dsa)
		DSA_free(dsa);
	if (pk)
		EVP_PKEY_free(pk);

	if (!pqg_consumed && p)
		BN_free(p);
	if (!pqg_consumed && q)
		BN_free(q);
	if (!pqg_consumed && g)
		BN_free(g);
	if (!key_consumed && y)
		BN_free(y);
	if (!sig_consumed && r)
		BN_free(r);
	if (!sig_consumed && s)
		BN_free(s);

	return ret;
}

static int openssl_dsa_keygen_en(struct dsa_pqggen_data *pqg, struct buffer *Y,
				 void **privkey)
{
	DSA *dsa = NULL;
	BUFFER_INIT(X);
	int ret;

	//_openssl_dsa_pqg_gen_public_api(&data->P, &data->Q, &data->G,
	//				      data->L));

	CKINT(_openssl_dsa_keygen(&pqg->P, &pqg->Q, &pqg->G, pqg->safeprime,
				  &X, Y, &dsa));

	*privkey = dsa;

out:
	free_buf(&X);
	return ret;
}

static void openssl_dsa_free_key(void *privkey)
{
	DSA *key = (DSA *)privkey;

	if (key)
		DSA_free(key);
}

static int openssl_dsa_siggen(struct dsa_siggen_data *data,
			      flags_t parsed_flags)
{
	struct dsa_pqggen_data *pqg = &data->pqg;
	EVP_MD_CTX *ctx = NULL;
	EVP_PKEY *pk = NULL;
	const EVP_MD *md = NULL;
	DSA *dsa = NULL;
	DSA_SIG *sig = NULL;
	const BIGNUM *r, *s;
	int ret = 0;
	unsigned int sig_len;
	unsigned char sig_buf[1024];
	const unsigned char *sig_buf_p = sig_buf;

	(void)parsed_flags;

	if (!data->privkey) {
		logger(LOGGER_ERR, "Private key missing\n");
		return -EINVAL;
	}

	dsa = data->privkey;

	logger(LOGGER_DEBUG, "cipher = %" PRIu64 "\n", data->cipher);
	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	//logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len, "msg");

	pk = EVP_PKEY_new();
	CKNULL(pk, -ENOMEM);

	EVP_PKEY_set1_DSA(pk, dsa);

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -ENOMEM);

	if (!EVP_SignInit_ex(ctx, md, NULL)) {
		ret = -EFAULT;
		goto out;
	}

	if (!EVP_SignUpdate(ctx, data->msg.buf, data->msg.len)) {
		ret = -EFAULT;
		goto out;
	}

	if (sizeof(sig_buf) < (unsigned long)EVP_PKEY_size(pk)) {
		logger(LOGGER_ERR,
		       "Programming error, buffer size insufficient\n");
		ret = -ENOMEM;
		goto out;
	}
	if (!EVP_SignFinal(ctx, sig_buf, &sig_len, pk)) {
		ret = -EFAULT;
		goto out;
	}

	d2i_DSA_SIG(&sig, &sig_buf_p, sig_len);

	openssl_dsa_SIG_get0(sig, &r, &s);

	CKINT(openssl_bn2buf(r, &data->R, pqg->N / 8));
	CKINT(openssl_bn2buf(s, &data->S, pqg->N / 8));

#if 0
	/* There was an error at one time where the verification failed! */
	{
		struct dsa_sigver_data ver;

		ver.L = data->L;
		ver.N = data->N;
		ver.cipher = data->cipher;
		ver.msg = data->msg;
		ver.P = data->P;
		ver.Q = data->Q;
		ver.G = data->G;
		ver.Y = data->Y;
		ver.R = data->R;
		ver.S = data->S;

		CKINT(openssl_dsa_sigver(&ver, parsed_flags));

		if (!ver.sigver_success) {
			logger(LOGGER_ERR,
			       "Verification of generated signature failed!\n");

			logger_binary(LOGGER_ERR, data->P.buf, data->P.len,
				      "P");
			logger_binary(LOGGER_ERR, data->Q.buf, data->Q.len,
				      "Q");
			logger_binary(LOGGER_ERR, data->G.buf, data->G.len,
				      "G");
			logger_binary(LOGGER_ERR, data->Y.buf, data->Y.len,
				      "Y");
			logger_binary(LOGGER_ERR, data->R.buf, data->R.len,
				      "R");
			logger_binary(LOGGER_ERR, data->S.buf, data->S.len,
				      "S");

			ret = -EFAULT;
			goto out;
		}
	}
#endif

	ret = 0;

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);
	if (pk)
		EVP_PKEY_free(pk);
	if (sig)
		DSA_SIG_free(sig);

	return ret;
}

static struct dsa_backend openssl_dsa =
{
	openssl_dsa_keygen,	/* dsa_keygen */
	openssl_dsa_keyver,
	openssl_dsa_siggen,	/* dsa_siggen */
	openssl_dsa_sigver,	/* dsa_sigver */
	openssl_dsa_pqg,	/* dsa_pqg */
	openssl_dsa_pqggen,
	openssl_dsa_keygen_en,
	openssl_dsa_free_key
};

ACVP_DEFINE_CONSTRUCTOR(openssl_dsa_backend)
static void openssl_dsa_backend(void)
{
	register_dsa_impl(&openssl_dsa);
}


/************************************************
 * ECDSA cipher interface functions
 ************************************************/

/* Internal key gen function */
static int _openssl_ecdsa_keygen(uint64_t curve, EC_KEY **out_key)
{
	EC_KEY *key = NULL;
	int ret = 0, nid = 0;

	CKINT_LOG(_openssl_ecdsa_curves(curve, &nid, NULL),
		  "Conversion of curve failed\n");

	if (!(key = EC_KEY_new_by_curve_name(nid))) {
		logger(LOGGER_ERR, "EC_KEY_new_by_curve_name() failed\n");
		ret = -EFAULT;
		goto out;
	}

	if (!EC_KEY_generate_key(key)) {
		logger(LOGGER_ERR, "EC_KEY_generate_key() failed\n");
		ret = -EFAULT;
		goto out;
	}

	*out_key = key;

out:
	return ret;
}

static int ec_get_pubkey(EC_KEY *key, BIGNUM *x, BIGNUM *y)
{
	const EC_POINT *pt;
	const EC_GROUP *grp;
	const EC_METHOD *meth;
	int rv = 0;
	BN_CTX *ctx;
	ctx = BN_CTX_new();

	if (!ctx)
		return -EFAULT;

	grp = EC_KEY_get0_group(key);
	pt = EC_KEY_get0_public_key(key);
	meth = EC_GROUP_method_of(grp);
	if (EC_METHOD_get_field_type(meth) == NID_X9_62_prime_field)
		rv = EC_POINT_get_affine_coordinates_GFp(grp, pt, x, y, ctx);
	else
#ifdef OPENSSL_NO_EC2M
	{
		fprintf(stderr, "ERROR: GF2m not supported\n");
		BN_CTX_free(ctx);
		return -EFAULT;
	}
#else
		rv = EC_POINT_get_affine_coordinates_GF2m(grp, pt, x, y, ctx);
#endif

	BN_CTX_free(ctx);

	return rv ? 0 : -EFAULT;
}

static int openssl_ecdsa_keygen(struct ecdsa_keygen_data *data,
				flags_t parsed_flags)
{
	EC_KEY *key = NULL;
	const BIGNUM *d = NULL;
	BIGNUM *Qx = NULL, *Qy = NULL;
	int ret = 0;
	size_t dbufferlen, xbufferlen, ybufferlen;

	(void)parsed_flags;

	Qx = BN_new();
	CKNULL(Qx, -ENOMEM);
	Qy = BN_new();
	CKNULL(Qy, -ENOMEM);

	CKINT(_openssl_ecdsa_keygen(data->cipher, &key));

	CKINT(ec_get_pubkey(key, Qx, Qy));

	d = EC_KEY_get0_private_key(key);

	ecdsa_get_bufferlen(data->cipher, &dbufferlen, &xbufferlen,
			    &ybufferlen);
	CKINT(alloc_buf(dbufferlen, &data->d));
	CKINT(alloc_buf(xbufferlen, &data->Qx));
	CKINT(alloc_buf(ybufferlen, &data->Qy));

	BN_bn2bin(Qx, data->Qx.buf - BN_num_bytes(Qx) + data->Qx.len);
	BN_bn2bin(Qy, data->Qy.buf - BN_num_bytes(Qy) + data->Qy.len);
	BN_bn2bin(d, data->d.buf - BN_num_bytes(d) + data->d.len);

	logger_binary(LOGGER_DEBUG, data->Qx.buf, data->Qx.len, "Qx");
	logger_binary(LOGGER_DEBUG, data->Qy.buf, data->Qy.len, "Qy");
	logger_binary(LOGGER_DEBUG, data->d.buf, data->d.len, "d");

out:
	if (key)
		EC_KEY_free(key);
	if (Qx)
		BN_free(Qx);
	if (Qy)
		BN_free(Qy);

	return ret;
}

static int openssl_ecdsa_pkvver(struct ecdsa_pkvver_data *data,
				flags_t parsed_flags)
{
	int nid = NID_undef, ret = 0;
	BIGNUM *Qx = NULL, *Qy = NULL;
	EC_KEY *key = NULL;

	(void)parsed_flags;

	logger_binary(LOGGER_DEBUG, data->Qx.buf, data->Qx.len, "Qx");
	logger_binary(LOGGER_DEBUG, data->Qy.buf, data->Qy.len, "Qy");

	Qx = BN_bin2bn((const unsigned char *)data->Qx.buf, (int)data->Qx.len,
		       Qx);
	CKNULL(Qx, -ENOMEM);

	Qy = BN_bin2bn((const unsigned char *)data->Qy.buf, (int)data->Qy.len,
		       Qy);
	CKNULL(Qy, -ENOMEM);

	CKINT(_openssl_ecdsa_curves(data->cipher, &nid, NULL));

	key = EC_KEY_new_by_curve_name(nid);
	CKNULL(key, -ENOMEM);

	if (1 == EC_KEY_set_public_key_affine_coordinates(key, Qx, Qy)) {
		logger(LOGGER_DEBUG, "ECDSA key successfully verified\n");
		data->keyver_success = 1;
	} else {
		logger(LOGGER_DEBUG, "ECDSA key verification failed\n");
		data->keyver_success = 0;
	}

	ret = 0;

out:
	if (Qx)
		BN_free(Qx);
	if (Qy)
		BN_free(Qy);
	if (key)
		EC_KEY_free(key);

	return ret;
}

static int openssl_ecdsa_keygen_en(uint64_t curve, struct buffer *Qx_buf,
				   struct buffer *Qy_buf, void **privkey)
{
	EC_KEY *key = NULL;
	BIGNUM *Qx = NULL, *Qy = NULL;
	size_t dbufferlen, xbufferlen, ybufferlen;
	int ret;

	Qx = BN_new();
	CKNULL(Qx, -ENOMEM);
	Qy = BN_new();
	CKNULL(Qy, -ENOMEM);

	CKINT(_openssl_ecdsa_keygen(curve, &key));

	CKINT(ec_get_pubkey(key, Qx, Qy));

	ecdsa_get_bufferlen(curve, &dbufferlen, &xbufferlen, &ybufferlen);
	CKINT(alloc_buf(xbufferlen, Qx_buf));
	CKINT(alloc_buf(ybufferlen, Qy_buf));

	BN_bn2bin(Qx, Qx_buf->buf - BN_num_bytes(Qx) + Qx_buf->len);
	BN_bn2bin(Qy, Qy_buf->buf - BN_num_bytes(Qy) + Qy_buf->len);

	logger_binary(LOGGER_DEBUG, Qx_buf->buf, Qx_buf->len, "Qx");
	logger_binary(LOGGER_DEBUG, Qy_buf->buf, Qy_buf->len, "Qy");

	*privkey = key;

out:
	if (ret && key)
		EC_KEY_free(key);
	if (Qx)
		BN_free(Qx);
	if (Qy)
		BN_free(Qy);
	return ret;
}

static void openssl_ecdsa_free_key(void *privkey)
{
	EC_KEY *ecdsa = (EC_KEY *)privkey;

	if (ecdsa)
		EC_KEY_free(ecdsa);
}

// TODO add ECDSA siggen primitive

static int openssl_ecdsa_siggen(struct ecdsa_siggen_data *data,
				flags_t parsed_flags)
{
	EVP_MD_CTX *ctx = NULL;
	EVP_PKEY *pk = NULL;
	const EVP_MD *md = NULL;
	ECDSA_SIG *sig = NULL;
	const BIGNUM *R, *S;
	int ret = 0;
	EC_KEY *key;
	unsigned int sig_len;
	unsigned char sig_buf[1024];
	const unsigned char *sig_buf_p = sig_buf;
	size_t dbufferlen, xbufferlen, ybufferlen;

	(void)parsed_flags;

	if (!data->privkey) {
		logger(LOGGER_ERR, "Private key missing\n");
		return -EINVAL;
	}

	key = data->privkey;

	pk = EVP_PKEY_new();
	CKNULL(pk, -ENOMEM);

	EVP_PKEY_set1_EC_KEY(pk, key);

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -EFAULT);

	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	if (!EVP_SignInit_ex(ctx, md, NULL)) {
		ret = -EFAULT;
		goto out;
	}

	if (!EVP_SignUpdate(ctx, data->msg.buf, data->msg.len)) {
		ret = -EFAULT;
		goto out;
	}

	if (!EVP_SignFinal(ctx, sig_buf, &sig_len, pk)) {
		ret = -EFAULT;
		goto out;
	}

	d2i_ECDSA_SIG(&sig, &sig_buf_p, sig_len);

	openssl_ecdsa_SIG_get0(sig, &R, &S);

	ecdsa_get_bufferlen(data->cipher, &dbufferlen, &xbufferlen,
			    &ybufferlen);
	CKINT(alloc_buf(xbufferlen, &data->R));
	CKINT(alloc_buf(xbufferlen, &data->S));

	BN_bn2bin(R,  data->R.buf -  BN_num_bytes(R) +  data->R.len);
	BN_bn2bin(S,  data->S.buf -  BN_num_bytes(S) +  data->S.len);

	logger_binary(LOGGER_DEBUG, data->R.buf, data->R.len, "R");
	logger_binary(LOGGER_DEBUG, data->S.buf, data->S.len, "S");

	ret = 0;

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);
	if (pk)
		EVP_PKEY_free(pk);
	if (sig)
		ECDSA_SIG_free(sig);

	return ret;
}

static int openssl_ecdsa_convert(struct ecdsa_sigver_data *data,
				 ECDSA_SIG **sig_out, EC_KEY **key_out)
{
	ECDSA_SIG *sig = NULL;
	EC_KEY *key = NULL;
	BIGNUM *Qx = NULL, *Qy = NULL, *R = NULL, *S = NULL;
	int ret, nid = NID_undef;

	logger_binary(LOGGER_DEBUG, data->R.buf, data->R.len, "R");
	logger_binary(LOGGER_DEBUG, data->S.buf, data->S.len, "S");

	sig = ECDSA_SIG_new();
	CKNULL(sig, -EFAULT);

	R = BN_bin2bn((const unsigned char *) data->R.buf, (int)data->R.len,
		      NULL);
	CKNULL(R, -EFAULT);

	S = BN_bin2bn((const unsigned char *) data->S.buf, (int)data->S.len,
		      NULL);
	CKNULL(S, -EFAULT);

	CKINT_O(openssl_ecdsa_SIG_set0(sig, R, S));

	CKINT(_openssl_ecdsa_curves(data->cipher, &nid, NULL));

	key = EC_KEY_new_by_curve_name(nid);
	CKNULL(key, -EFAULT);

	logger_binary(LOGGER_DEBUG, data->Qx.buf, data->Qx.len, "Qx");
	logger_binary(LOGGER_DEBUG, data->Qy.buf, data->Qy.len, "Qy");

	Qx = BN_bin2bn((const unsigned char *) data->Qx.buf, (int)data->Qx.len,
		       NULL);
	CKNULL(Qx, -EFAULT);

	Qy = BN_bin2bn((const unsigned char *) data->Qy.buf, (int)data->Qy.len,
		       NULL);
	CKNULL(Qy, -EFAULT);

	CKINT_O(EC_KEY_set_public_key_affine_coordinates(key, Qx, Qy));

	*key_out = key;
	*sig_out = sig;

	ret = 0;

out:
	if (ret) {
		if (sig)
			ECDSA_SIG_free(sig);
		if (key)
			EC_KEY_free(key);
	}

	if (Qx)
		BN_free(Qx);
	if (Qy)
		BN_free(Qy);
	return ret;
}

static int
openssl_ecdsa_sigver_primitive(struct ecdsa_sigver_data *data,
			       flags_t parsed_flags)
{
	EVP_PKEY_CTX *ctx = NULL;
	EVP_PKEY *key = NULL;
	EC_KEY *ec_key = NULL;
	ECDSA_SIG *sig = NULL;
	unsigned char *der_sig = NULL;
	size_t der_sig_len;
	int ret;

	(void)parsed_flags;

	CKINT(openssl_ecdsa_convert(data, &sig, &ec_key));

	der_sig_len = (size_t)i2d_ECDSA_SIG(sig, &der_sig);

	if (!der_sig_len) {
		logger(LOGGER_ERR, "Failure to convert signature into DER\n");
		ret = -EFAULT;
		goto out;
	}

	key = EVP_PKEY_new();
	CKNULL(key, -ENOMEM);
	EVP_PKEY_set1_EC_KEY(key, ec_key);

	ctx = EVP_PKEY_CTX_new(key, NULL);
	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate PKEY context\n");

	CKINT_O_LOG(EVP_PKEY_verify_init(ctx), "PKEY verify init failed\n");

	ret = EVP_PKEY_verify(ctx, der_sig, der_sig_len, data->msg.buf,
			      data->msg.len);
	if (ret == 1) {
		logger(LOGGER_DEBUG, "Signature verification successful\n");
		data->sigver_success = 1;
	} else {
		logger(LOGGER_DEBUG, "Signature verification failed %s\n",
		       ERR_error_string(ERR_get_error(), NULL));
		data->sigver_success = 0;
	}

	ret = 0;

out:
	if (der_sig)
		free(der_sig);
	if (sig)
		ECDSA_SIG_free(sig);
	if (ec_key)
		EC_KEY_free(ec_key);
	if (key)
		EVP_PKEY_free(key);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	return ret;
}

static int openssl_ecdsa_sigver(struct ecdsa_sigver_data *data,
				flags_t parsed_flags)
{
	EVP_MD_CTX *ctx = NULL;
	const EVP_MD *md = NULL;
	EVP_PKEY *pk = NULL;
	ECDSA_SIG *sig = NULL;
	EC_KEY *key = NULL;
	unsigned int sig_len;
	unsigned char sig_buf[1024];
	unsigned char *sig_buf_p = sig_buf;
	int ret = 0;

	if (data->component)
		return openssl_ecdsa_sigver_primitive(data, parsed_flags);

	CKINT(openssl_ecdsa_convert(data, &sig, &key));

	pk = EVP_PKEY_new();
	CKNULL(pk, -ENOMEM);

	EVP_PKEY_set1_EC_KEY(pk, key);

	sig_len = (unsigned int)i2d_ECDSA_SIG(sig, &sig_buf_p);

	ctx = EVP_MD_CTX_create();
	CKNULL(ctx, -ENOMEM);

	CKINT(openssl_md_convert(data->cipher & ACVP_HASHMASK, &md));

	if (!EVP_VerifyInit_ex(ctx, md, NULL)) {
		ret = -EFAULT;
		goto out;
	}

	if (!EVP_VerifyUpdate(ctx, data->msg.buf, data->msg.len)) {
		ret = -EFAULT;
		goto out;
	}

	ret = EVP_VerifyFinal(ctx, sig_buf, sig_len, pk);
	if (!ret) {
		logger(LOGGER_DEBUG, "Signature verification: signature bad\n");
		data->sigver_success = 0;
	} else if (ret == 1) {
		logger(LOGGER_DEBUG,
		       "Signature verification: signature good\n");
		data->sigver_success = 1;
		ret = 0;
	} else {
		logger(LOGGER_WARN,
		       "Signature verification: general error\n");
		ret = -EFAULT;
	}

out:
	if (ctx)
		EVP_MD_CTX_destroy(ctx);
	if (sig)
		ECDSA_SIG_free(sig);
	if (key)
		EC_KEY_free(key);
	if (pk)
		EVP_PKEY_free(pk);

	return ret;
}

static struct ecdsa_backend openssl_ecdsa =
{
	openssl_ecdsa_keygen,   /* ecdsa_keygen_testing */
	NULL,
	openssl_ecdsa_pkvver,   /* ecdsa_pkvver */
	openssl_ecdsa_siggen,   /* ecdsa_siggen */
	openssl_ecdsa_sigver,   /* ecdsa_sigver */
	openssl_ecdsa_keygen_en,
	openssl_ecdsa_free_key,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_ecdsa_backend)
static void openssl_ecdsa_backend(void)
{
	register_ecdsa_impl(&openssl_ecdsa);
}

/************************************************
 * DH interface functions
 ************************************************/
static int openssl_dh_ss_common(uint64_t cipher,
				uint64_t safeprime,
				struct buffer *P,
				struct buffer *Q,
				struct buffer *G,
				struct buffer *Yrem,
				struct buffer *Xloc,
				struct buffer *Yloc,
				struct buffer *hashzz)
{
	DH *dh = NULL;
	BIGNUM *bn_Yrem = NULL, *bn_Xloc = NULL, *bn_Yloc = NULL;
	const BIGNUM *cbn_Xloc = NULL, *cbn_Yloc = NULL;
	BUFFER_INIT(ss);
	unsigned int localkey_consumed = 0;
	size_t keylen = 0;
	int ret = 0;

	/* Generate the parameters to be used */
	dh = DH_new();
	CKNULL_LOG(dh, -ENOMEM, "DH_new() failed");

	CKINT(openssl_dh_set_param(P, Q, G, safeprime, dh, &keylen));

	logger_binary(LOGGER_DEBUG, Yrem->buf, Yrem->len, "Yrem");
	bn_Yrem = BN_bin2bn((const unsigned char *)Yrem->buf, (int)Yrem->len,
			    NULL);
	CKNULL_LOG(bn_Yrem, -ENOMEM, "BN_bin2bn() failed\n");

	if (!Xloc->len || !Yloc->len) {
		CKINT_O_LOG(DH_generate_key(dh), "DH_generate_key failed: %s\n",
			    ERR_error_string(ERR_get_error(), NULL));

		openssl_dh_get0_key(dh, &cbn_Yloc, &cbn_Xloc);

		CKINT(openssl_bn2buffer(cbn_Yloc, Yloc));
		logger_binary(LOGGER_DEBUG, Yloc->buf, Yloc->len,
			      "generated Yloc");
	} else {
		logger_binary(LOGGER_DEBUG, Xloc->buf, Xloc->len, "used Xloc");
		bn_Xloc = BN_bin2bn((const unsigned char *)Xloc->buf,
				    (int)Xloc->len, NULL);
		CKNULL_LOG(bn_Xloc, -ENOMEM, "BN_bin2bn() failed\n");

		CKINT_O_LOG(openssl_dh_set0_key(dh, NULL, bn_Xloc),
			    "DH_set0_key failed\n");
		localkey_consumed = 1;
	}

	CKINT_LOG(alloc_buf(keylen, &ss), "Cannot allocate ss\n");

	/* Compute the shared secret */
	if (0 > DH_compute_key_padded(ss.buf, bn_Yrem, dh)) {
		logger(LOGGER_DEBUG, "Cannot generate shared secret %s\n",
		       ERR_error_string(ERR_get_error(), NULL));

		/*
		 * This error may be possible if the key does not match PQG.
		 * In this case, the test is successful nonetheless.
		 */
		ret = -EOPNOTSUPP;
		goto out;
	}
	logger_binary(LOGGER_DEBUG, ss.buf, ss.len, "Generated shared secret");

	/* We do not use CKINT here, because -ENOENT is no real error */
	ret = openssl_hash_ss(cipher, &ss, hashzz);

out:
	if (dh)
		DH_free(dh);

	if (bn_Yrem)
		BN_free(bn_Yrem);

	if (!localkey_consumed && bn_Xloc)
		BN_free(bn_Xloc);
	if (!localkey_consumed && bn_Yloc)
		BN_free(bn_Yloc);

	free_buf(&ss);

	return ret;
}

static int openssl_dh_ss(struct dh_ss_data *data, flags_t parsed_flags)
{
	(void)parsed_flags;

	return openssl_dh_ss_common(data->cipher, data->safeprime,
				    &data->P, &data->Q, &data->G,
				    &data->Yrem,
				    &data->Xloc, &data->Yloc,
				    &data->hashzz);
}

static int openssl_dh_ss_ver(struct dh_ss_ver_data *data,
			       flags_t parsed_flags)
{
	int ret = openssl_dh_ss_common(data->cipher, data->safeprime,
				       &data->P, &data->Q,
				       &data->G,
				       &data->Yrem,
				       &data->Xloc, &data->Yloc,
				       &data->hashzz);

	(void)parsed_flags;

	if (ret == -EOPNOTSUPP || ret == -ENOENT) {
		data->validity_success = 0;
		logger(LOGGER_DEBUG, "DH validity test failed\n");
		return 0;
	} else if (!ret) {
		data->validity_success = 1;
		logger(LOGGER_DEBUG, "DH validity test passed\n");
		return 0;
	}

	logger(LOGGER_DEBUG, "DH validity test: general error\n");
	return ret;
}

static struct dh_backend openssl_dh =
{
	openssl_dh_ss,
	openssl_dh_ss_ver,
	openssl_dh_keygen,
	openssl_dh_keyver
};

ACVP_DEFINE_CONSTRUCTOR(openssl_dh_backend)
static void openssl_dh_backend(void)
{
	register_dh_impl(&openssl_dh);
}

/************************************************
 * ECDH cipher interface functions
 ************************************************/

static int openssl_ecdh_ss_common(uint64_t cipher,
				  struct buffer *Qxrem, struct buffer *Qyrem,
				  struct buffer *privloc,
				  struct buffer *Qxloc, struct buffer *Qyloc,
				  struct buffer *hashzz)
{

	EC_KEY *local_key = NULL;
	EC_POINT *remote_pubkey = NULL;
	BN_CTX *c = NULL;
	size_t dbufferlen, xbufferlen, ybufferlen;
	const BIGNUM *d = NULL;
	BIGNUM *Qx = NULL, *Qy = NULL, *localQx = NULL, *localQy = NULL,
	       *locald = NULL;
	EC_GROUP *group = NULL;
	BUFFER_INIT(ss);
	int nid = 0, ret = 0;

	ecdsa_get_bufferlen(cipher, &dbufferlen, &xbufferlen,
			    &ybufferlen);

	CKINT_LOG(_openssl_ecdsa_curves(cipher, &nid, NULL),
		  "Conversion of curve failed\n");

	Qx = BN_bin2bn((const unsigned char *)Qxrem->buf, (int)Qxrem->len, Qx);
	CKNULL(Qx, -ENOMEM);

	Qy = BN_bin2bn((const unsigned char *)Qyrem->buf, (int)Qyrem->len, Qy);
	CKNULL(Qy, -ENOMEM);

	/* Generate point of remote public key */
	group = EC_GROUP_new_by_curve_name(nid);
	CKNULL(group, -ENOMEM);

	remote_pubkey = EC_POINT_new(group);
	CKNULL_LOG(remote_pubkey, -ENOMEM, "EC_POINT_new() failed\n");
	c = BN_CTX_new();
	CKNULL_LOG(c, -ENOMEM, "BN_CTX_new failed\n");

	if (EC_METHOD_get_field_type(EC_GROUP_method_of(group))
	    == NID_X9_62_prime_field) {
		CKINT_O(EC_POINT_set_affine_coordinates_GFp(group,
							    remote_pubkey,
							    Qx, Qy, c));
	} else {
#ifdef OPENSSL_NO_EC2M
		logger(LOGGER_WARN, "GF2m not supported\n");
		ret = -EFAULT;
		goto out;
#else
		CKINT_O(EC_POINT_set_affine_coordinates_GF2m(group,
							     remote_pubkey,
							     Qx, Qy, c));
#endif
	}

	local_key = EC_KEY_new_by_curve_name(nid);
	CKNULL_LOG(local_key, -ENOMEM, "EC_KEY_new_by_curve_name() failed\n");
	EC_KEY_set_flags(local_key, EC_FLAG_COFACTOR_ECDH);

	if (!privloc->len || !Qxloc->len || !Qyloc->len) {
		/* Create our own local key */
		free_buf(privloc);
		CKINT(alloc_buf(dbufferlen, privloc));

		if (!Qxloc->len)
			CKINT(alloc_buf(xbufferlen, Qxloc));

		if (!Qyloc->len)
			CKINT(alloc_buf(ybufferlen, Qyloc));

		CKINT_O_LOG(EC_KEY_generate_key(local_key),
			    "Cannot generate local key %s\n",
			    ERR_error_string(ERR_get_error(), NULL));

		localQx = BN_new();
		CKNULL(localQx, -ENOMEM);
		localQy = BN_new();
		CKNULL(localQy, -ENOMEM);

		CKINT(ec_get_pubkey(local_key, localQx, localQy));

		if (BN_num_bytes(localQx) > (int)Qxloc->len) {
			logger(LOGGER_ERR,
			       "BUG: OpenSSL Qx longer (%u) than expected (%zu)\n",
			       BN_num_bytes(localQx), Qxloc->len);
			ret = -EFAULT;
			goto out;
		}
		BN_bn2bin(localQx,
			  Qxloc->buf - BN_num_bytes(localQx) + Qxloc->len);
		if (BN_num_bytes(localQy) > (int)Qyloc->len) {
			logger(LOGGER_ERR,
			       "BUG: OpenSSL Qx longer (%u) than expected (%zu)\n",
			       BN_num_bytes(localQy), Qyloc->len);
			ret = -EFAULT;
			goto out;
		}
		BN_bn2bin(localQy,
			  Qyloc->buf - BN_num_bytes(localQy) + Qyloc->len);

		d = EC_KEY_get0_private_key(local_key);

		if (BN_num_bytes(d) > (int)privloc->len) {
			logger(LOGGER_ERR,
			       "BUG: OpenSSL privkey longer (%u) than expected (%zu)\n",
			       BN_num_bytes(d), privloc->len);
			ret = -EFAULT;
			goto out;
		}
		BN_bn2bin(d, privloc->buf - BN_num_bytes(d) + privloc->len);

		logger_binary(LOGGER_DEBUG, Qxloc->buf, Qxloc->len,
			      "generated local Qx");
		logger_binary(LOGGER_DEBUG, Qyloc->buf, Qyloc->len,
			      "generated local Qy");
		logger_binary(LOGGER_DEBUG, privloc->buf, privloc->len,
			      "generated local private key");
	} else {
		/* Use existing local key */

		localQx = BN_bin2bn((const unsigned char *)Qxloc->buf,
				    (int)Qxloc->len, localQx);
		CKNULL(localQx, -ENOMEM);

		localQy = BN_bin2bn((const unsigned char *)Qyloc->buf,
				    (int)Qyloc->len, localQy);
		CKNULL(localQy, -ENOMEM);

		locald = BN_bin2bn((const unsigned char *)privloc->buf,
				    (int)privloc->len, locald);
		CKNULL(localQy, -ENOMEM);

		ret = EC_KEY_set_private_key(local_key, locald);
		if (ret != 1) {
			ret = -EOPNOTSUPP;
			goto out;
		}

		ret = EC_KEY_set_public_key_affine_coordinates(local_key,
							       localQx,
							       localQy);
		if (ret != 1) {
			logger(LOGGER_DEBUG,
			       "EC_KEY_set_public_key_affine_coordinates failed: %s\n",
			       ERR_error_string(ERR_get_error(), NULL));
			ret = -EOPNOTSUPP;
			goto out;
		}
	}

	/* Create buffer for shared secret */
	CKINT(alloc_buf((size_t)(EC_GROUP_get_degree(group) + 7)/8, &ss));

	if (0 == ECDH_compute_key(ss.buf, ss.len, remote_pubkey,
				  local_key, NULL)) {
		logger(LOGGER_DEBUG, "Cannot generate shared secret %s\n",
		       ERR_error_string(ERR_get_error(), NULL));

		/*
		 * This error may be possible if the point is not on the curve.
		 * In this case, the test is successful nonetheless.
		 */
		ret = -EOPNOTSUPP;
		goto out;
	}
	logger_binary(LOGGER_DEBUG, ss.buf, ss.len, "Generated shared secret");

	/* We do not use CKINT here, because -ENOENT is no real error */
	ret = openssl_hash_ss(cipher, &ss, hashzz);

out:
	if (c)
		BN_CTX_free(c);
	if (remote_pubkey)
		EC_POINT_free(remote_pubkey);
	if (Qx)
		BN_free(Qx);
	if (Qy)
		BN_free(Qy);
	if (localQx)
		BN_free(localQx);
	if (localQy)
		BN_free(localQy);
	if (locald)
		BN_free(locald);
	if (local_key)
		EC_KEY_free(local_key);
	if (group)
		EC_GROUP_free(group);

	free_buf(&ss);

	return ret;
}

static int openssl_ecdh_ss(struct ecdh_ss_data *data, flags_t parsed_flags)
{
	(void)parsed_flags;

	return openssl_ecdh_ss_common(data->cipher, &data->Qxrem, &data->Qyrem,
				      &data->privloc,
				      &data->Qxloc, &data->Qyloc,
				      &data->hashzz);
}

static int openssl_ecdh_ss_ver(struct ecdh_ss_ver_data *data,
			       flags_t parsed_flags)
{
	int ret = openssl_ecdh_ss_common(data->cipher, &data->Qxrem,
					 &data->Qyrem,
					 &data->privloc,
					 &data->Qxloc, &data->Qyloc,
					 &data->hashzz);

	(void)parsed_flags;

	if (ret == -EOPNOTSUPP || ret == -ENOENT) {
		data->validity_success = 0;
		logger(LOGGER_DEBUG, "ECDH validity test failed\n");
		return 0;
	} else if (!ret) {
		data->validity_success = 1;
		logger(LOGGER_DEBUG, "ECDH validity test passed\n");
		return 0;
	}

	logger(LOGGER_DEBUG, "ECDH validity test: general error\n");
	return ret;
}

static struct ecdh_backend openssl_ecdh =
{
	openssl_ecdh_ss,
	openssl_ecdh_ss_ver,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_ecdh_backend)
static void openssl_ecdh_backend(void)
{
	register_ecdh_impl(&openssl_ecdh);
}

/************************************************
 * SP800-56B rev 2 KTS IFC cipher interface functions
 ************************************************/

/*
 * return: 0 on success, < 0 on true error, > 0 when validation fails
 */
static int openssl_rsa_kas_ifc_encrypt_common(struct kts_ifc_data *data,
					      int validation)
{
	EVP_PKEY_CTX *ctx = NULL;
	EVP_PKEY *pk = NULL;
	RSA *rsa = NULL;
	BIGNUM *n = NULL, *e = NULL;
	BUFFER_INIT(label);
	BUFFER_INIT(new_c);
	struct buffer *dkm_p, *c_p;
	size_t outlen, keylen = (data->keylen) ? data->keylen : data->modulus;
	int ret;

	if (keylen > data->modulus)
		return -EINVAL;

	rsa = RSA_new();
	CKNULL(rsa, -ENOMEM);

	if (validation) {
		struct kts_ifc_init_validation_data *init_val =
					&data->u.kts_ifc_init_validation;

		CKINT(left_pad_buf(&init_val->n, data->modulus >> 3));

		dkm_p = &init_val->dkm;
		c_p = &new_c;

		if (init_val->p.buf && init_val->q.buf) {
			BIGNUM *p = NULL, *q = NULL;
			p = BN_bin2bn((const unsigned char *)init_val->p.buf,
				      (int)init_val->p.len, p);
			CKNULL(p, -ENOMEM);
			q = BN_bin2bn((const unsigned char *)init_val->q.buf,
				      (int)init_val->q.len, e);
			CKNULL(q, -ENOMEM);

			CKINT_O_LOG(openssl_rsa_set0_factors(rsa, p, q),
				    "Assembly of RSA factors failed\n");
		}

		n = BN_bin2bn((const unsigned char *)init_val->n.buf,
			      (int)init_val->n.len, n);
		CKNULL(n, -ENOMEM);
		e = BN_bin2bn((const unsigned char *)init_val->e.buf,
			      (int)init_val->e.len, e);
		CKNULL(e, -ENOMEM);
	} else {
		struct kts_ifc_init_data *init = &data->u.kts_ifc_init;

		CKINT(left_pad_buf(&init->n, data->modulus >> 3));
		if (!init->dkm.len) {
			CKINT(alloc_buf(keylen >> 3, &init->dkm));
			RAND_bytes(init->dkm.buf, (int)init->dkm.len);

			/*
			 * Ensure that in case of raw encryption, the value is
			 * not too large.
			 */
			init->dkm.buf[0] &= ~0x80;
		}

		dkm_p = &init->dkm;
		c_p = &init->iut_c;

		n = BN_bin2bn((const unsigned char *)init->n.buf,
			      (int)init->n.len, n);
		CKNULL(n, -ENOMEM);
		e = BN_bin2bn((const unsigned char *)init->e.buf,
			      (int)init->e.len, e);
		CKNULL(e, -ENOMEM);
	}

	CKINT_O_LOG(openssl_rsa_set0_key(rsa, n, e, NULL),
		    "Assembly of RSA key failed\n");

	pk = EVP_PKEY_new();
	CKNULL(pk, -ENOMEM);

	EVP_PKEY_set1_RSA(pk, rsa);

	ctx = EVP_PKEY_CTX_new(pk, NULL);
	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate PKEY context\n");

	CKINT_O_LOG(EVP_PKEY_encrypt_init(ctx), "PKEY encrypt init failed\n");

	if (data->kts_hash) {
		/* OAEP Padding */
		const EVP_MD *md = NULL;

		CKINT(openssl_md_convert(data->kts_hash, &md));
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(ctx,
						RSA_PKCS1_OAEP_PADDING),
			    "Setting OAEP padding failed\n");
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_oaep_md(ctx, md),
			   "Setting of OAEP MD failed\n");

		/* Evaluate encoding and concatenate Server and IUT Ids */

		if (convert_cipher_match(data->kts_encoding,
					 ACVP_KAS_ENCODING_CONCATENATION,
					 ACVP_CIPHERTYPE_KAS)) {
			CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_mgf1_md(ctx, md),
				    "Setting MFGL MD failed\n");
			CKINT(alloc_buf(data->server_id.len + data->iut_id.len,
					&label));
			memcpy(label.buf, data->iut_id.buf, data->iut_id.len);
			memcpy(label.buf + data->iut_id.len, data->server_id.buf,
			data->server_id.len);


			CKINT_O_LOG(EVP_PKEY_CTX_set0_rsa_oaep_label(ctx,
								     label.buf,
								     label.len),
				    "Setting OAEP label failed\n");
		}
	} else {
		/* Raw encryption */
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_NO_PADDING),
			    "Setting no padding failed\n");
	}

	/* Determine buffer length */
	CKINT_O_LOG(EVP_PKEY_encrypt(ctx, NULL, &outlen, dkm_p->buf,
				     dkm_p->len),
		    "Getting ciphertext length failed %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	CKINT(alloc_buf(outlen, c_p));

	ret = EVP_PKEY_encrypt(ctx, c_p->buf, &outlen, dkm_p->buf, dkm_p->len);


	if (validation) {
		struct kts_ifc_init_validation_data *init_val =
					&data->u.kts_ifc_init_validation;

		/* OpenSSL returns 0 on failure */
		if (ret != 1) {
			logger(LOGGER_DEBUG,
			       "Validation: RSA encryption failed %s\n",
			       ERR_error_string(ERR_get_error(), NULL));
			ret = EFAULT;
		} else if (outlen != init_val->c.len ||
			   memcmp(init_val->c.buf, c_p->buf, outlen)) {
			logger(LOGGER_DEBUG, "lens %zu %zu\n", outlen,
			       init_val->c.len);
			logger_binary(LOGGER_DEBUG, init_val->c.buf,
				      init_val->c.len,
				      "expected encrypted secret");
			logger_binary(LOGGER_DEBUG, c_p->buf, c_p->len,
				      "calculated encrypted secret");

			ret = EFAULT;
		} else {
			ret = 0;
		}
	} else if (ret != 1) {
		logger(LOGGER_ERR, "RSA encryption failed %s\n",
		       ERR_error_string(ERR_get_error(), NULL));
		ret = -EFAULT;
	} else {
		ret = 0;
	}

out:
	if (pk)
		EVP_PKEY_free(pk);
	if (rsa)
		RSA_free(rsa);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);
	free_buf(&new_c);

	/*
	 * The man page for EVP_PKEY_CTX_set0_rsa_oaep_label reads:
	 *
	 * "The library takes ownership of the label so the caller should
	 * not free the original memory pointed to by label."
	 *
	 * So, this call is not needed.
	 * free_buf(&label);
	 */

	return ret;
}

static int openssl_rsa_kas_ifc_set_key(RSA *rsa,
				       struct buffer *n_buf,
				       struct buffer *e_buf,
				       struct buffer *d_buf,
				       struct buffer *p_buf,
				       struct buffer *q_buf)
{
	BIGNUM *n = NULL, *e = NULL, *d = NULL, *p = NULL, *q = NULL;
	int ret;

	n = BN_bin2bn((const unsigned char *)n_buf->buf, (int)n_buf->len, n);
	CKNULL(n, -ENOMEM);
	e = BN_bin2bn((const unsigned char *)e_buf->buf, (int)e_buf->len, e);
	CKNULL(e, -ENOMEM);
	d = BN_bin2bn((const unsigned char *)d_buf->buf, (int)d_buf->len, d);
	CKNULL(d, -ENOMEM);
	p = BN_bin2bn((const unsigned char *)p_buf->buf, (int)p_buf->len, p);
	CKNULL(p, -ENOMEM);
	q = BN_bin2bn((const unsigned char *)q_buf->buf, (int)q_buf->len, q);
	CKNULL(q, -ENOMEM);

	CKINT_O_LOG(openssl_rsa_set0_key(rsa, n, e, d),
		    "Assembly of RSA key failed\n");
	CKINT_O_LOG(openssl_rsa_set0_factors(rsa, p, q),
		    "Assembly of RSA factors failed\n");

out:
	return ret;
}

static int openssl_rsa_kas_ifc_decrypt_common(struct kts_ifc_data *data,
					      int validation)
{
	BUFFER_INIT(tmp);
	BUFFER_INIT(label);
	EVP_PKEY_CTX *ctx = NULL;
	EVP_PKEY *pk = NULL;
	RSA *rsa = NULL;

	struct buffer *c_p;
	size_t outlen, keylen = (data->keylen) ? data->keylen : data->modulus;
	int ret;

	if (keylen > data->modulus)
		return -EINVAL;

	rsa = RSA_new();
	CKNULL(rsa, -ENOMEM);

	if (validation) {
		struct kts_ifc_resp_validation_data *resp_val =
					&data->u.kts_ifc_resp_validation;

		CKINT(left_pad_buf(&resp_val->n, data->modulus >> 3));

		CKINT(openssl_rsa_kas_ifc_set_key(rsa, &resp_val->n,
						  &resp_val->e, &resp_val->d,
						  &resp_val->p, &resp_val->q));

		c_p = &resp_val->c;
	} else {
		struct kts_ifc_resp_data *resp = &data->u.kts_ifc_resp;

		CKINT(left_pad_buf(&resp->n, data->modulus >> 3));

		CKINT(openssl_rsa_kas_ifc_set_key(rsa, &resp->n,
						  &resp->e, &resp->d,
						  &resp->p, &resp->q));

		c_p = &resp->c;
	}

	pk = EVP_PKEY_new();
	CKNULL(pk, -ENOMEM);

	EVP_PKEY_set1_RSA(pk, rsa);

	ctx = EVP_PKEY_CTX_new(pk, NULL);
	CKNULL_LOG(ctx, -EFAULT, "Cannot allocate PKEY context\n");

	CKINT_O_LOG(EVP_PKEY_decrypt_init(ctx), "PKEY decrypt init failed\n");

	if (data->kts_hash) {
		/* OAEP Padding */
		const EVP_MD *md = NULL;

		CKINT(openssl_md_convert(data->kts_hash, &md));
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(ctx,
						RSA_PKCS1_OAEP_PADDING),
			    "Setting OAEP padding failed\n");
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_oaep_md(ctx, md),
			    "Setting of OAEP MD failed\n");

		/* Evaluate encoding and concatenate IUT and Server Ids */

		if (convert_cipher_match(data->kts_encoding,
					 ACVP_KAS_ENCODING_CONCATENATION,
					 ACVP_CIPHERTYPE_KAS)) {
			CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_mgf1_md(ctx, md),
				    "Setting MFGL MD failed\n");
			CKINT(alloc_buf(data->server_id.len + data->iut_id.len,
					&label));
			memcpy(label.buf, data->server_id.buf, data->server_id.len);
			memcpy(label.buf + data->server_id.len, data->iut_id.buf,
			data->iut_id.len);

			CKINT_O_LOG(EVP_PKEY_CTX_set0_rsa_oaep_label(ctx,
								     label.buf,
								     label.len),
				    "Setting OAEP label failed\n");
		}
	} else {
		/* Raw encryption */
		CKINT_O_LOG(EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_NO_PADDING),
			    "Setting padding failed\n");
	}

	/* Determine buffer length */
	CKINT_O_LOG(EVP_PKEY_decrypt(ctx, NULL, &outlen, c_p->buf, c_p->len),
		    "Getting plaintext length failed %s\n",
		    ERR_error_string(ERR_get_error(), NULL));

	CKINT(alloc_buf(outlen, &tmp));

	/* End of change */

	ret = EVP_PKEY_decrypt(ctx, tmp.buf, &tmp.len, c_p->buf, c_p->len);

	if (validation) {
		struct kts_ifc_resp_validation_data *resp_val =
					&data->u.kts_ifc_resp_validation;

		/* OpenSSL returns 0 on failure */
		if (ret != 1) {
			logger(LOGGER_DEBUG,
			       "Validation: RSA encryption failed %s\n",
			       ERR_error_string(ERR_get_error(), NULL));
			ret = EFAULT;
		} else if (outlen != resp_val->dkm.len ||
			   memcmp(resp_val->dkm.buf, tmp.buf, outlen)) {
			logger(LOGGER_DEBUG, "lens %zu %zu\n", outlen,
			       resp_val->dkm.len);
			logger_binary(LOGGER_DEBUG, resp_val->dkm.buf,
				      resp_val->dkm.len,
				      "expected decrypted secret");
			logger_binary(LOGGER_DEBUG, tmp.buf, tmp.len,
				      "calculated decrypted secret");

			ret = EFAULT;
		} else {
			ret = 0;
		}

	} else if (ret != 1) {
		logger(LOGGER_ERR, "RSA decryption failed %s\n",
		    ERR_error_string(ERR_get_error(), NULL));
		ret = -EFAULT;

	} else {
		struct kts_ifc_resp_data *resp = &data->u.kts_ifc_resp;

		if (tmp.len < (keylen >> 3)) {
			logger(LOGGER_ERR,
			       "RSA decrypted data has insufficient size\n");
			ret = -EFAULT;
			goto out;
		}

		CKINT(alloc_buf(keylen >> 3, &resp->dkm));
		memcpy(resp->dkm.buf, tmp.buf, resp->dkm.len);
	}

out:
	if (pk)
		EVP_PKEY_free(pk);
	if (rsa)
		RSA_free(rsa);
	if (ctx)
		EVP_PKEY_CTX_free(ctx);

	/*
	 * The man page for EVP_PKEY_CTX_set0_rsa_oaep_label reads:
	 *
	 * "The library takes ownership of the label so the caller should
	 * not free the original memory pointed to by label."
	 *
	 * So, this call is not needed.
	 * free_buf(&label);
	 */

	free_buf(&tmp);
	return ret;
}

static int openssl_kts_ifc_generate(struct kts_ifc_data *data,
				    flags_t parsed_flags)
{
	int ret;

	(void)parsed_flags;

	if ((parsed_flags & FLAG_OP_KAS_ROLE_INITIATOR) &&
	    (parsed_flags & FLAG_OP_AFT)) {
		CKINT(openssl_rsa_kas_ifc_encrypt_common(data, 0));
	} else if ((parsed_flags & FLAG_OP_KAS_ROLE_RESPONDER) &&
		   (parsed_flags & FLAG_OP_AFT)) {
		CKINT(openssl_rsa_kas_ifc_decrypt_common(data, 0));
	} else if ((parsed_flags & FLAG_OP_KAS_ROLE_INITIATOR) &&
		   (parsed_flags & FLAG_OP_VAL)) {
		struct kts_ifc_init_validation_data *init_val =
					&data->u.kts_ifc_init_validation;

		CKINT(openssl_rsa_kas_ifc_encrypt_common(data, 1));

		if (ret > 0) {
			init_val->validation_success = 0;
			ret = 0;
		} else {
			init_val->validation_success = 1;
		}
	} else if ((parsed_flags & FLAG_OP_KAS_ROLE_RESPONDER) &&
		   (parsed_flags & FLAG_OP_VAL)) {
		struct kts_ifc_resp_validation_data *resp_val =
					&data->u.kts_ifc_resp_validation;

		CKINT(openssl_rsa_kas_ifc_decrypt_common(data, 1));

		if (ret > 0) {
			resp_val->validation_success = 0;
			ret = 0;
		} else {
			resp_val->validation_success = 1;
		}
	} else {
		logger(LOGGER_ERR, "Unknown test\n");
		ret = -EINVAL;
	}

out:
	return ret;
}

static struct kts_ifc_backend openssl_kts_ifc =
{
	openssl_kts_ifc_generate,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_kts_ifc_backend)
static void openssl_kts_ifc_backend(void)
{
	register_kts_ifc_impl(&openssl_kts_ifc);
}

#ifdef OPENSSL_ENABLE_HKDF
/************************************************
 * SP800-56C rev1 cipher interface functions
 ************************************************/
static int openssl_hkdf_generate(struct hkdf_data *data,
				 flags_t parsed_flags)
{
	BUFFER_INIT(local_dkm);
	const EVP_MD *md = NULL;
	uint8_t secret[EVP_MAX_MD_SIZE];
	size_t mdlen;
	uint32_t derived_key_bytes = data->dkmlen / 8;
	int ret;

	(void)parsed_flags;

	CKINT(openssl_md_convert(data->hash & ACVP_HASHMASK, &md));
	mdlen = (size_t)EVP_MD_size(md);

	if (data->dkm.buf && data->dkm.len) {
		CKINT(alloc_buf(derived_key_bytes, &local_dkm));
	} else {
		CKINT(alloc_buf(derived_key_bytes, &data->dkm));
	}

	/* Extract phase */
	CKINT(openssl_hkdf_extract(md, data->z.buf, data->z.len,
				   data->salt.buf, data->salt.len,
				   secret, &mdlen));

	/* Expand phase */
	if (local_dkm.buf && local_dkm.len) {
		CKINT(openssl_hkdf_expand(md, data->info.buf, data->info.len,
					  secret, mdlen,
					  local_dkm.buf, &local_dkm.len));

		if (local_dkm.len != data->dkm.len ||
		    memcmp(local_dkm.buf, data->dkm.buf, local_dkm.len)) {
			logger(LOGGER_DEBUG, "HKDF validation result: fail\n");
			data->validity_success = 0;
		} else {
			data->validity_success = 1;
		}
	} else {
		CKINT(openssl_hkdf_expand(md, data->info.buf, data->info.len,
					  secret, mdlen,
					  data->dkm.buf, &data->dkm.len));
	}

out:
	free_buf(&local_dkm);

	return ret;
}

static struct hkdf_backend openssl_hkdf =
{
	openssl_hkdf_generate,
};

ACVP_DEFINE_CONSTRUCTOR(openssl_hkdf_backend)
static void openssl_hkdf_backend(void)
{
	register_hkdf_impl(&openssl_hkdf);
}
#endif /* OPENSSL_ENABLE_HKDF */
