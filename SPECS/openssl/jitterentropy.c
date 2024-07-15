/*
 * Jitterentropy provider for OpenSSL 3.0.
 * It pulls in-kernel FIPS compliant entropy "jitterentropy_rng" through
 * AF_ALG socket API.
 * Jitterentropy documentation:
 * http://www.chronox.de/jent/doc/CPU-Jitter-NPTRNG.pdf
 *
 * Copyright (C) 2022, VMware, Inc.
 * Author : Alexey Makhalov <amakhalov@vmware.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, GOOD TITLE or
 * NON INFRINGEMENT.  See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 * Based on the following openssl-3.0 code:
 *   providers/legacyprov.c
 *   providers/implementations/rands/seed_src.c
 *
 * Kernel requirements:
 *  - CONFIG_CRYPTO_JITTERENTROPY=y/m
 *  - CONFIG_CRYPTO_USER_API_RNG=y/m
 *
 * /etc/ssl/openssl.cnf configuration:
 *
 * [openssl_init]
 * random = random_sect
 * ...
 *
 * [random_sect]
 * seed = jitterentropy
 *
 * [provider_sect]
 * jitterentropy = jitterentropy_sect
 * ...
 *
 * [jitterentropy_sect]
 * activate = 1
 */

#include <unistd.h>
#include <stdio.h>
#include <stdint.h>
#include <errno.h>
#include <string.h>
#include <gnu/lib-names.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <linux/if_alg.h>
#include <openssl/core.h>
#include <openssl/core_dispatch.h>
#include <openssl/core_names.h>
#include <openssl/params.h>
#include <openssl/objects.h>
#include <openssl/err.h>
#include <openssl/provider.h>
#include <openssl/proverr.h>
#include <openssl/evp.h>

#define UNUSED(var)	(void)(var)

#ifdef DEBUG_LOGS
#define pr_dbg(fmt, ...) \
	do { \
		fprintf(stderr, "JENTROPY-DEBUG: [%s:%d] " fmt, \
                __func__, __LINE__, ##__VA_ARGS__); \
	} while (0)
#else
#define pr_dbg(fmt, ...)
#endif // DEBUG_LOGS

#define pr_err(fmt, ...) \
	do { \
		_pr_err(__LINE__, __func__, fmt, ##__VA_ARGS__); \
	} while (0)

static void _pr_err(int, const char *, const char *, ...);

/* Required to make this shared object executable */
const char service_interp[] __attribute__((section(".interp"))) = "/lib/" LD_SO;

/***********************************************************
 * API to the kernel                                       *
 ***********************************************************/

int algif_rng_open(int do_accept);
void algif_rng_close(int socket);
ssize_t algif_rng_get(int socket, uint8_t *buffer, size_t len);

static void _pr_err(int line, const char *func, const char *fmt, ...)
{
	va_list args;

	va_start(args, fmt);

	BIO *bio_err = BIO_new_fp(stderr, BIO_NOCLOSE);
	if (bio_err == NULL) {
        /* this is a fallback method, we should not miss errors */
		fprintf(stderr, "JENTROPY-ERROR: %s():%d ", func, line);
		vfprintf(stderr, fmt, args);
        va_end(args);
		return;
	}

	BIO_printf(bio_err, "JENTROPY-ERROR: %s():%d ", func, line);
	BIO_vprintf(bio_err, fmt, args);
	BIO_free(bio_err);
	va_end(args);
}

int algif_rng_open(int do_accept)
{
	struct sockaddr_alg sa;
	int sk, fd;
	pr_dbg("do_accept: %d\n", do_accept);

	sa.salg_family = AF_ALG;
	strcpy((char *)sa.salg_type, "rng");
	sa.salg_feat = 0;
	sa.salg_mask = 0;
	strcpy((char *)sa.salg_name, "jitterentropy_rng");

	sk = socket(AF_ALG, SOCK_SEQPACKET, 0);
	if (sk == -1) {
		pr_err("ERROR: socket(...) failed ...('%s')\n", strerror(errno));
		return 0;
	}

	if (bind(sk, (struct sockaddr *)&sa, sizeof(sa)) == -1) {
		pr_err("ERROR: bind(...) failed ...('%s')\n", strerror(errno));
		close(sk);
		return 0;
	}

	if (!do_accept)
		return sk;

	fd = accept(sk, NULL, 0);
	close(sk);
	if (fd == -1) {
		pr_err("ERROR: accept(...) failed ...('%s')\n", strerror(errno));
		return 0;
	}

	return fd;
}

void algif_rng_close(int socket)
{
	pr_dbg("\n");
	close(socket);
}

ssize_t algif_rng_get(int socket, uint8_t *buffer, size_t len)
{
	ssize_t out = 0;
	struct iovec iov;
	struct msghdr msg;

	pr_dbg("len: %ld\n", len);

	while (len) {
		ssize_t r = 0;

		iov.iov_base = (void *)(uintptr_t)buffer;
		iov.iov_len = len;
		msg.msg_name = NULL;
		msg.msg_namelen = 0;
		msg.msg_control = NULL;
		msg.msg_controllen = 0;
		msg.msg_flags = 0;
		msg.msg_iov = &iov;
		msg.msg_iovlen = 1;

		r = recvmsg(socket, &msg, 0);
		pr_dbg("recvmsg: (r: %ld) (len: %lu) (out: %ld)\n", r, len, out);
		if (r <= 0) {
			if (r < 0 || len > 0) {
				pr_err("ERROR: recvmsg(...) failed ...('%s')\n", strerror(errno));
			}
			break;
		}
		len -= (size_t)r;
		out += r;
		buffer += r;
	}

	pr_dbg("out: %ld\n", out);

	return out;
}

/***********************************************************
 * Provider API to the OpenSSL                             *
 ***********************************************************/

static OSSL_FUNC_rand_newctx_fn rand_newctx;
static OSSL_FUNC_rand_freectx_fn rand_freectx;
static OSSL_FUNC_rand_instantiate_fn rand_instantiate;
static OSSL_FUNC_rand_uninstantiate_fn rand_uninstantiate;
static OSSL_FUNC_rand_generate_fn rand_generate;
static OSSL_FUNC_rand_reseed_fn rand_reseed;
static OSSL_FUNC_rand_gettable_ctx_params_fn rand_gettable_ctx_params;
static OSSL_FUNC_rand_get_ctx_params_fn rand_get_ctx_params;
static OSSL_FUNC_rand_verify_zeroization_fn rand_verify_zeroization;
static OSSL_FUNC_rand_lock_fn rand_lock;
static OSSL_FUNC_rand_unlock_fn rand_unlock;
static OSSL_FUNC_rand_get_seed_fn rand_get_seed;
static OSSL_FUNC_rand_clear_seed_fn rand_clear_seed;

typedef struct {
	void *provctx;
	int state;
} PROV_SEED_SRC;

static void *rand_newctx(void *provctx, void *parent,
		const OSSL_DISPATCH *parent_dispatch)
{
	PROV_SEED_SRC *s;

	UNUSED(parent_dispatch);

	pr_dbg("\n");

	if (parent != NULL) {
		pr_err("ERROR: parent == NULL\n");
		ERR_raise(ERR_LIB_PROV, PROV_R_SEED_SOURCES_MUST_NOT_HAVE_A_PARENT);
		return NULL;
	}

	s = OPENSSL_zalloc(sizeof(*s));
	if (s == NULL) {
		pr_err("ERROR: OPENSSL_zalloc\n");
		ERR_raise(ERR_LIB_PROV, ERR_R_MALLOC_FAILURE);
		return NULL;
	}

	s->provctx = provctx;
	s->state = EVP_RAND_STATE_UNINITIALISED;
	return s;
}

static void rand_freectx(void *vseed)
{
	pr_dbg("\n");
	OPENSSL_free(vseed);
}

static int rand_instantiate(void *vseed, unsigned int strength,
		int prediction_resistance,
		const unsigned char *pstr, size_t pstr_len,
		ossl_unused const OSSL_PARAM params[])
{
	PROV_SEED_SRC *s = (PROV_SEED_SRC *)vseed;

	UNUSED(strength);
	UNUSED(prediction_resistance);
	UNUSED(pstr);
	UNUSED(pstr_len);

	pr_dbg("\n");

	s->state = EVP_RAND_STATE_READY;
	return 1;
}

static int rand_uninstantiate(void *vseed)
{
	PROV_SEED_SRC *s = (PROV_SEED_SRC *)vseed;

	pr_dbg("\n");

	s->state = EVP_RAND_STATE_UNINITIALISED;
	return 1;
}

static int rand_generate(void *vseed, unsigned char *out, size_t outlen,
		unsigned int strength,
		ossl_unused int prediction_resistance,
		ossl_unused const unsigned char *adin,
		ossl_unused size_t adin_len)
{
	int socket, ret;
	PROV_SEED_SRC *s = (PROV_SEED_SRC *)vseed;

	UNUSED(strength);

	pr_dbg("\n");

	if (s->state != EVP_RAND_STATE_READY) {
		pr_err("ERROR: s->state != EVP_RAND_STATE_READY\n");
		ERR_raise(ERR_LIB_PROV,
				s->state == EVP_RAND_STATE_ERROR ? PROV_R_IN_ERROR_STATE
				: PROV_R_NOT_INSTANTIATED);
		return 0;
	}

	socket = algif_rng_open(1);
	if (!socket) {
		pr_err("ERROR: socket = 0\n");
		ERR_raise(ERR_LIB_PROV, PROV_R_NOT_SUPPORTED);
		return 0;
	}

	ret = algif_rng_get(socket, out, outlen);
	algif_rng_close(socket);

	return ret;
}

static int rand_reseed(void *vseed,
		ossl_unused int prediction_resistance,
		ossl_unused const unsigned char *ent,
		ossl_unused size_t ent_len,
		ossl_unused const unsigned char *adin,
		ossl_unused size_t adin_len)
{
	PROV_SEED_SRC *s = (PROV_SEED_SRC *)vseed;

	if (s->state != EVP_RAND_STATE_READY) {
		pr_err("ERROR: s->state != EVP_RAND_STATE_READY\n");
		ERR_raise(ERR_LIB_PROV,
				s->state == EVP_RAND_STATE_ERROR ? PROV_R_IN_ERROR_STATE
				: PROV_R_NOT_INSTANTIATED);
		return 0;
	}
	return 1;
}

static int rand_get_ctx_params(void *vseed, OSSL_PARAM params[])
{
	PROV_SEED_SRC *s = (PROV_SEED_SRC *)vseed;
	OSSL_PARAM *p;

	pr_dbg("\n");

	p = OSSL_PARAM_locate(params, OSSL_RAND_PARAM_STATE);
	if (p != NULL && !OSSL_PARAM_set_int(p, s->state))
		return 0;

	p = OSSL_PARAM_locate(params, OSSL_RAND_PARAM_STRENGTH);
	if (p != NULL && !OSSL_PARAM_set_int(p, 1024))
		return 0;

	p = OSSL_PARAM_locate(params, OSSL_RAND_PARAM_MAX_REQUEST);
	if (p != NULL && !OSSL_PARAM_set_size_t(p, 128))
		return 0;
	return 1;
}

static const OSSL_PARAM *rand_gettable_ctx_params(ossl_unused void *vseed,
		ossl_unused void *provctx)
{
	static const OSSL_PARAM known_gettable_ctx_params[] = {
		OSSL_PARAM_int(OSSL_RAND_PARAM_STATE, NULL),
		OSSL_PARAM_uint(OSSL_RAND_PARAM_STRENGTH, NULL),
		OSSL_PARAM_size_t(OSSL_RAND_PARAM_MAX_REQUEST, NULL),
		OSSL_PARAM_END
	};

	pr_dbg("\n");

	return known_gettable_ctx_params;
}

static int rand_lock(ossl_unused void *vctx)
{
	pr_dbg("\n");
	return 1;
}

static void rand_unlock(ossl_unused void *vctx)
{
	pr_dbg("\n");
}

static int rand_verify_zeroization(ossl_unused void *vseed)
{
	pr_dbg("\n");
	return 1;
}

static size_t rand_get_seed(void *vseed, unsigned char **pout,
		int entropy, size_t min_len, size_t max_len,
		int prediction_resistance,
		const unsigned char *adin, size_t adin_len)
{
	size_t bytes_needed;
	unsigned char *p;

	pr_dbg("entropy: %d min_len: %lu max_len: %lu\n",
			entropy, min_len, max_len);

	pr_dbg("prediction_resistance: %d adin_len: %lu\n",
			prediction_resistance, adin_len);

	/*
	 * Figure out how many bytes we need.
	 * This assumes that the seed sources provide eight bits of entropy
	 * per byte.  For lower quality sources, the formula will need to be
	 * different.
	 */
	bytes_needed = entropy >= 0 ? (entropy + 7) / 8 : 0;
	if (bytes_needed < min_len)
		bytes_needed = min_len;
	if (bytes_needed > max_len) {
		pr_err("ERROR: bytes_needed > max_len\n");
		ERR_raise(ERR_LIB_PROV, PROV_R_ENTROPY_SOURCE_STRENGTH_TOO_WEAK);
		return 0;
	}

	p = OPENSSL_secure_malloc(bytes_needed);
	if (p == NULL) {
		pr_err("ERROR: p == NULL\n");
		ERR_raise(ERR_LIB_PROV, ERR_R_MALLOC_FAILURE);
		return 0;
	}
	if (rand_generate(vseed, p, bytes_needed, 0, prediction_resistance,
				adin, adin_len) != 0) {
		*pout = p;
		return bytes_needed;
	}
	OPENSSL_secure_clear_free(p, bytes_needed);
	return 0;
}

static void rand_clear_seed(ossl_unused void *vdrbg,
		unsigned char *out, size_t outlen)
{
	pr_dbg("\n");
	OPENSSL_secure_clear_free(out, outlen);
}

const OSSL_DISPATCH rand_functions[] = {
	{ OSSL_FUNC_RAND_NEWCTX, (void(*)(void))rand_newctx },
	{ OSSL_FUNC_RAND_FREECTX, (void(*)(void))rand_freectx },
	{ OSSL_FUNC_RAND_INSTANTIATE, (void(*)(void))rand_instantiate },
	{ OSSL_FUNC_RAND_UNINSTANTIATE, (void(*)(void))rand_uninstantiate },
	{ OSSL_FUNC_RAND_GENERATE, (void(*)(void))rand_generate },
	{ OSSL_FUNC_RAND_RESEED, (void(*)(void))rand_reseed },
	{ OSSL_FUNC_RAND_LOCK, (void(*)(void))rand_lock },
	{ OSSL_FUNC_RAND_UNLOCK, (void(*)(void))rand_unlock },
	{ OSSL_FUNC_RAND_GETTABLE_CTX_PARAMS, (void(*)(void))rand_gettable_ctx_params },
	{ OSSL_FUNC_RAND_GET_CTX_PARAMS, (void(*)(void))rand_get_ctx_params },
	{ OSSL_FUNC_RAND_VERIFY_ZEROIZATION, (void(*)(void))rand_verify_zeroization },
	{ OSSL_FUNC_RAND_GET_SEED, (void(*)(void))rand_get_seed },
	{ OSSL_FUNC_RAND_CLEAR_SEED, (void(*)(void))rand_clear_seed },
	{ 0, NULL }
};

static const OSSL_ALGORITHM jitterentropy_rands[] = {
	{ "jitterentropy", "fips=yes", rand_functions, NULL },
	{ NULL, NULL, NULL, NULL }
};

typedef struct prov_ctx_st {
	const OSSL_CORE_HANDLE *handle;
	OSSL_LIB_CTX *libctx;
	BIO_METHOD *corebiometh;
} PROV_CTX;
#define PROV_LIBCTX_OF(provctx) (((PROV_CTX *)provctx)->libctx)

/*
 * Forward declarations to ensure that interface functions are correctly
 * defined.
 */
static OSSL_FUNC_provider_gettable_params_fn jitterentropy_gettable_params;
static OSSL_FUNC_provider_get_params_fn jitterentropy_get_params;
static OSSL_FUNC_provider_query_operation_fn jitterentropy_query;

/* Parameters we provide to the core */
static const OSSL_PARAM jitterentropy_param_types[] = {
	OSSL_PARAM_DEFN(OSSL_PROV_PARAM_NAME, OSSL_PARAM_UTF8_PTR, NULL, 0),
	OSSL_PARAM_DEFN(OSSL_PROV_PARAM_VERSION, OSSL_PARAM_UTF8_PTR, NULL, 0),
	OSSL_PARAM_END
};

static void jitterentropy_teardown(void *provctx)
{
	pr_dbg("\n");
	if (provctx) {
		OSSL_LIB_CTX_free(PROV_LIBCTX_OF(provctx));
		OPENSSL_free(provctx);
	}
}

static const OSSL_PARAM *jitterentropy_gettable_params(void *provctx)
{
	UNUSED(provctx);
	pr_dbg("\n");
	return jitterentropy_param_types;
}

static int jitterentropy_get_params(void *provctx, OSSL_PARAM params[])
{
	OSSL_PARAM *p;

	UNUSED(provctx);
	pr_dbg("\n");

	p = OSSL_PARAM_locate(params, OSSL_PROV_PARAM_NAME);
	if (p != NULL && !OSSL_PARAM_set_utf8_ptr(p, "OpenSSL Jitter Entropy Provider"))
		return 0;
	p = OSSL_PARAM_locate(params, OSSL_PROV_PARAM_VERSION);
	if (p != NULL && !OSSL_PARAM_set_utf8_ptr(p, "0.1"))
		return 0;
	return 1;
}

static const OSSL_ALGORITHM *jitterentropy_query(void *provctx, int operation_id,
		int *no_cache)
{
	*no_cache = 0;

	UNUSED(provctx);
	pr_dbg("\n");

	if (operation_id == OSSL_OP_RAND)
		return jitterentropy_rands;

	return NULL;
}

/* Functions we provide to the core */
static const OSSL_DISPATCH jitterentropy_dispatch_table[] = {
	{ OSSL_FUNC_PROVIDER_TEARDOWN, (void (*)(void))jitterentropy_teardown },
	{ OSSL_FUNC_PROVIDER_GETTABLE_PARAMS, (void (*)(void))jitterentropy_gettable_params },
	{ OSSL_FUNC_PROVIDER_GET_PARAMS, (void (*)(void))jitterentropy_get_params },
	{ OSSL_FUNC_PROVIDER_QUERY_OPERATION, (void (*)(void))jitterentropy_query },
	{ 0, NULL }
};

/* Provider entry point */
int OSSL_provider_init(const OSSL_CORE_HANDLE *handle,
		const OSSL_DISPATCH *in,
		const OSSL_DISPATCH **out,
		void **provctx)
{
	OSSL_LIB_CTX *libctx = NULL;
	int socket;

	/* Probe Kernel support */
	socket = algif_rng_open(0);
	if (!socket) {
		pr_err("ERROR: algif_rng_open (%s)\n", strerror(errno));
		ERR_raise(ERR_LIB_PROV, PROV_R_NOT_SUPPORTED);
		return 0;
	}
	algif_rng_close(socket);

	if ((*provctx = OPENSSL_zalloc(sizeof(PROV_CTX))) == NULL
		|| (libctx = OSSL_LIB_CTX_new_child(handle, in)) == NULL)
	{
		OSSL_LIB_CTX_free(libctx);
		jitterentropy_teardown(*provctx);
		*provctx = NULL;
		return 0;
	}
	((PROV_CTX *)*provctx)->libctx = libctx;
	((PROV_CTX *)*provctx)->handle = handle;

	*out = jitterentropy_dispatch_table;

	return 1;
}

/* Standalone executable entry point */
int main(void)
{
	int socket;

	printf("Jitterentropy provider for OpenSSL 3.0\n");
	printf("Probing kernel capabilities: ");
	socket = algif_rng_open(1);
	if (!socket) {
		fprintf(stderr, "FAILED\n");
		fprintf(stderr, "\n  Please make sure kernel supports AF_ALG socket type and \"jitterentropy_rng\""
				"\n  crypto rng (should be present in /proc/crypto)\n");
		_exit(1);
	}

	printf("PASSED\n");
	printf("\n  To verify openssl is using this provider as entropy source, run:"
			"\n  'strace -e socket,bind,accept,recvmsg openssl rand -hex 20'\n");
	algif_rng_close(socket);
	_exit(0);
}
