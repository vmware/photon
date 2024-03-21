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

#include <stdlib.h>

#include "backend_common.h"

#include <hash.h>
#include <hmac.h>
#include <sha256.h>
#include <sha512.h>
#include <sha3.h>

/************************************************
 * SHA cipher interface functions
 ************************************************/
static int acvpproxy_hash_convert(uint64_t cipher, const struct hash **ret_hash)
{
	const struct hash *hash;

	switch (cipher) {
	case ACVP_SHA256:
	case ACVP_HMACSHA2_256:
		hash = sha256;
		break;
	case ACVP_SHA512:
	case ACVP_HMACSHA2_512:
		hash = sha512;
		break;
	case ACVP_SHA3_224:
	case ACVP_HMACSHA3_224:
		hash = sha3_224;
		break;
	case ACVP_SHA3_256:
	case ACVP_HMACSHA3_256:
		hash = sha3_256;
		break;
	case ACVP_SHA3_384:
	case ACVP_HMACSHA3_384:
		hash = sha3_384;
		break;
	case ACVP_SHA3_512:
	case ACVP_HMACSHA3_512:
		hash = sha3_512;
		break;
	default:
		logger(LOGGER_ERR, "Cipher implementation not found\n");
		return -EOPNOTSUPP;
	}

	*ret_hash = hash;
	return 0;
}

static int acvpproxy_sha_generate(struct sha_data *data, flags_t parsed_flags)
{
	HASH_CTX_ON_STACK(ctx);
	const struct hash *hash;
	int ret;

	(void)parsed_flags;

	CKINT(acvpproxy_hash_convert(data->cipher, &hash));

	CKINT(alloc_buf(hash->digestsize, &data->mac));

	hash->init(ctx);
	hash->update(ctx, data->msg.buf, data->msg.len);
	hash->final(ctx, data->mac.buf);

out:
	return ret;
}

static struct sha_backend acvpproxy_sha =
{
	acvpproxy_sha_generate,   /* hash_generate */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(acvpproxy_sha_backend)
static void acvpproxy_sha_backend(void)
{
	register_sha_impl(&acvpproxy_sha);
}

/************************************************
 * HMAC cipher interface functions
 ************************************************/
static int acvpproxy_mac_generate(struct hmac_data *data, flags_t parsed_flags)
{
	const struct hash *hash;
	int ret;

	(void)parsed_flags;

	CKINT(acvpproxy_hash_convert(data->cipher, &hash));

	CKINT(alloc_buf(hash->digestsize, &data->mac));

	hmac(hash, data->key.buf, data->key.len,
	     data->msg.buf, data->msg.len,
	     data->mac.buf);

	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "HMAC");

out:
	return ret;
}

static struct hmac_backend acvpproxy_mac =
{
	acvpproxy_mac_generate,
};

ACVP_DEFINE_CONSTRUCTOR(acvpproxy_mac_backend)
static void acvpproxy_mac_backend(void)
{
	register_hmac_impl(&acvpproxy_mac);
}
