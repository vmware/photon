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

#define _GNU_SOURCE
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/utsname.h>

#include "backend_common.h"
#include "logger.h"
#include "stringhelper.h"

/* cipher types of the kernel crypto API */
#define ABLKCIPHER	0x00000001
#define SHASH		0x00000002
#define DRBG		0x00000008

#define TYPE_KEEP	0x01000000 /* keep cipher mode open, needed
				      for Monte Carlo cipher tests
				      which need the chaining mode
				      state */
#define TYPE_ENC	0x02000000 /* Encryption operation */
#define TYPE_DEC	0x04000000 /* Decryption operation */

#define KCAPI_SYSFS "/sys/kernel/debug/kcapi_lrng/"

/*************************************************
 * Helper functions
 *************************************************/

static int kcapi_writedata(const char *name, struct buffer *buf)
{
	int out = -1;
	char *filename = NULL;
	int ret = 0;

	if (!buf->buf || !buf->len)
		return 0;

	filename = calloc(1, (strlen(KCAPI_SYSFS) + strlen(name) + 1));
	CKNULL(filename, -ENOMEM);

	sprintf(filename, "%s%s", KCAPI_SYSFS, name);

	out = open(filename, O_WRONLY);
	if (out < 0) {
		ret = -errno;
		printf("Cannot open file %s for writing: %s\n", filename,
		       strerror(errno));
		goto out;
	}

	if (-1 == write(out, buf->buf, buf->len)) {
		ret = -errno;
		printf("Cannot write data to %s: %s\n", filename,
		       strerror(errno));
		goto out;
	}

out:

	if (out >= 0)
		close(out);
	if (filename)
		free(filename);
	return ret;

}

static int kcapi_writeu32(char *name, uint32_t val)
{
	char string[11];
	struct buffer tmp;

	if (!val)
		return 0;

	memset(string, 0, sizeof(string));
	snprintf(string, sizeof(string), "%u", val);
	tmp.buf = (uint8_t *)string;
	tmp.len = sizeof(string);

	return kcapi_writedata(name, &tmp);
}

static int kcapi_readdata(char *name, struct buffer *buf)
{
	int in = -1;
	char *filename = NULL;
	int ret = 0;
	ssize_t readdata = 0;

	if (!buf->buf || !buf->len)
		return 0;

	filename = calloc(1, (strlen(KCAPI_SYSFS) + strlen(name) + 1));
	CKNULL(filename, -ENOMEM);

	sprintf(filename, "%s%s", KCAPI_SYSFS, name);

	in = open(filename, O_RDONLY);
	if (in < 0) {
		ret = -errno;
		logger(LOGGER_VERBOSE, "Cannot open file %s for reading: %s\n",
		       filename, strerror(errno));
		goto out;
	}

	memset(buf->buf, 0, buf->len);
	readdata = read(in, buf->buf, buf->len);
	if (readdata < 0) {
		ret = -errno;
		logger(LOGGER_VERBOSE, "Cannot read data from %s: %s\n",
		       filename, strerror(errno));
		goto out;
	}
	buf->len = (size_t)readdata;

out:
	if (in >= 0)
		close(in);
	if (filename)
		free(filename);
	return ret;

}

/************************************************
 * Symmetric cipher interface functions
 ************************************************/

static int kcapi_rawciphername(uint64_t cipher, char **cipherstring)
{
	char *outstr = NULL;

	outstr = calloc(1, 128);
	if (!outstr)
		return -EFAULT;
	switch (cipher) {
	case ACVP_ECB:
		sprintf(outstr, "ecb(aes)");
		break;

	case ACVP_HMACSHA1:
		sprintf(outstr, "hmac(sha1)");
		break;
	case ACVP_HMACSHA2_224:
		sprintf(outstr, "hmac(sha224)");
		break;
	case ACVP_HMACSHA2_256:
		sprintf(outstr, "hmac(sha256)");
		break;
	case ACVP_HMACSHA2_384:
		sprintf(outstr, "hmac(sha384)");
		break;
	case ACVP_HMACSHA2_512:
		sprintf(outstr, "hmac(sha512)");
		break;

	case ACVP_SHA1:
		sprintf(outstr, "sha1");
		break;
	case ACVP_SHA224:
		sprintf(outstr, "sha224");
		break;
	case ACVP_SHA256:
		sprintf(outstr, "sha256");
		break;
	case ACVP_SHA384:
		sprintf(outstr, "sha384");
		break;
	case ACVP_SHA512:
		sprintf(outstr, "sha512");
		break;

	default:
		logger(LOGGER_WARN, "Unknown cipher %" PRIu64 "\n", cipher);
		free(outstr);
		return -EFAULT;
	}
	*cipherstring = outstr;

	return 0;
}

static int kcapi_ciphername(uint64_t cipher, char **cipherstring)
{
	char *envstr = NULL;
	char *outstr = NULL;

	switch (cipher) {
	case ACVP_ECB:
		envstr = secure_getenv("KCAPI_ECB_AES");
		break;

	case ACVP_HMACSHA1:
		envstr = secure_getenv("KCAPI_HMAC_SHA1");
		break;
	case ACVP_HMACSHA2_224:
		envstr = secure_getenv("KCAPI_HMAC_SHA224");
		break;
	case ACVP_HMACSHA2_256:
		envstr = secure_getenv("KCAPI_HMAC_SHA256");
		break;
	case ACVP_HMACSHA2_384:
		envstr = secure_getenv("KCAPI_HMAC_SHA384");
		break;
	case ACVP_HMACSHA2_512:
		envstr = secure_getenv("KCAPI_HMAC_SHA512");
		break;

	case ACVP_SHA1:
		envstr = secure_getenv("KCAPI_SHA1");
		break;
	case ACVP_SHA224:
		envstr = secure_getenv("KCAPI_SHA224");
		break;
	case ACVP_SHA256:
		envstr = secure_getenv("KCAPI_SHA256");
		break;
	case ACVP_SHA384:
		envstr = secure_getenv("KCAPI_SHA384");
		break;
	case ACVP_SHA512:
		envstr = secure_getenv("KCAPI_SHA512");
		break;

	default:
		logger(LOGGER_ERR, "Unknown cipher\n");
		return -EFAULT;
	}

	if (envstr) {
		outstr = strdup(envstr);
		if (!outstr)
			return -EFAULT;
		*cipherstring = outstr;
		return 0;
	} else {
		return kcapi_rawciphername(cipher, cipherstring);
	}
}

static int kcapi_setupcipher(struct sym_data *data, uint32_t type)
{
	char *ciphername = NULL;
	struct buffer tmp;
	int ret;

	CKINT(kcapi_ciphername(data->cipher, &ciphername));

	tmp.buf = (uint8_t *)ciphername;
	tmp.len = strlen(ciphername);
	CKINT(kcapi_writedata("name", &tmp));
	logger(LOGGER_VERBOSE, "name = %s\n", ciphername);

	CKINT(kcapi_writeu32("type", type));
	logger(LOGGER_VERBOSE, "type = %u\n", type);

	CKINT(kcapi_writedata("key", &data->key));
	logger_binary(LOGGER_VERBOSE, data->key.buf, data->key.len, "key");

	CKINT(kcapi_writedata("iv", &data->iv));
	logger_binary(LOGGER_VERBOSE, data->iv.buf, data->iv.len, "iv");

out:
	if (ciphername)
		free(ciphername);
	return ret;
}

static int kcapi_mct_init(struct sym_data *data, flags_t parsed_flags)
{
	if (parsed_flags & FLAG_OP_ENC)
		return kcapi_setupcipher(data, ABLKCIPHER | TYPE_ENC);
	else
		return kcapi_setupcipher(data, ABLKCIPHER | TYPE_DEC);
}

static int kcapi_mct_update(struct sym_data *data, flags_t parsed_flags)
{
	int ret;
	(void)parsed_flags;

	CKINT(kcapi_writedata("data", &data->data));
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "data written");
	CKINT(kcapi_readdata("data", &data->data));
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "data read");

out:
	return ret;
}

static int kcapi_mct_fini(struct sym_data *data, flags_t parsed_flags)
{
	(void)data;
	(void)parsed_flags;
	return 0;
}

static int kcapi_encrypt(struct sym_data *data, flags_t parsed_flags)
{
	int ret;

	(void)parsed_flags;

	CKINT(kcapi_setupcipher(data, ABLKCIPHER | TYPE_ENC));
	CKINT(kcapi_writedata("data", &data->data));
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "data written");
	CKINT(kcapi_readdata("data", &data->data));
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "data read");

out:
	return ret;
}

static int kcapi_decrypt(struct sym_data *data, flags_t parsed_flags)
{
	int ret;

	(void)parsed_flags;

	CKINT(kcapi_setupcipher(data, ABLKCIPHER | TYPE_DEC));
	CKINT(kcapi_writedata("data", &data->data));
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "data written");
	CKINT(kcapi_readdata("data", &data->data));
	logger_binary(LOGGER_DEBUG, data->data.buf, data->data.len,
		      "data read");

out:
	return ret;
}

static struct sym_backend kcapi_sym =
{
	kcapi_encrypt,		/* encrypt */
	kcapi_decrypt,		/* decrypt */
	kcapi_mct_init,		/* mct_init */
	kcapi_mct_update,	/* mct_update */
	kcapi_mct_fini,		/* mct_fini */
};

ACVP_DEFINE_CONSTRUCTOR(kcapi_sym_backend)
static void kcapi_sym_backend(void)
{
	register_sym_impl(&kcapi_sym);
}

/************************************************
 * HMAC cipher interface functions
 ************************************************/

#define KCAPI_MAX_DIGESTSIZE	64
static int kcapi_hmac_generate(struct hmac_data *data, flags_t parsed_flags)
{
	char *ciphername = NULL;
	struct buffer tmp;
	int ret;

	(void)parsed_flags;

	CKINT(kcapi_ciphername(data->cipher, &ciphername));

	tmp.buf = (uint8_t *)ciphername;
	tmp.len = strlen(ciphername);
	CKINT(kcapi_writedata("name", &tmp));
	logger(LOGGER_VERBOSE, "name = %s\n", ciphername);

	CKINT(kcapi_writeu32("type", SHASH));
	logger(LOGGER_VERBOSE, "type = %u\n", SHASH);

	CKINT(kcapi_writedata("key", &data->key));
	logger_binary(LOGGER_VERBOSE, data->key.buf, data->key.len, "key");

	CKINT(kcapi_writedata("data", &data->msg));
	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len,
		      "data written");

	CKINT(alloc_buf(KCAPI_MAX_DIGESTSIZE, &data->mac));

	CKINT(kcapi_readdata("data", &data->mac));
	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "data read");

	ret = 0;

out:
	if (ciphername)
		free(ciphername);
	return ret;
}

static struct hmac_backend kcapi_hmac =
{
	kcapi_hmac_generate,	/* hmac_generate */
};

ACVP_DEFINE_CONSTRUCTOR(kcapi_hmac_backend)
static void kcapi_hmac_backend(void)
{
	register_hmac_impl(&kcapi_hmac);
}

/************************************************
 * SHA cipher interface functions
 ************************************************/

static int kcapi_sha_generate(struct sha_data *data, flags_t parsed_flags)
{
	char *ciphername = NULL;
	struct buffer tmp;
	int ret;

	(void)parsed_flags;

	CKINT(kcapi_ciphername(data->cipher, &ciphername));
	tmp.buf = (uint8_t *)ciphername;
	tmp.len = strlen(ciphername);
	CKINT(kcapi_writedata("name", &tmp));
	logger(LOGGER_VERBOSE, "name = %s\n", ciphername);

	CKINT(kcapi_writeu32("type", SHASH));
	logger(LOGGER_VERBOSE, "type = %u\n", SHASH);

	CKINT(kcapi_writedata("data", &data->msg));
	logger_binary(LOGGER_DEBUG, data->msg.buf, data->msg.len,
		      "data written");

	CKINT(alloc_buf(KCAPI_MAX_DIGESTSIZE, &data->mac));

	CKINT(kcapi_readdata("data", &data->mac));
	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len,
		      "data read");

	ret = 0;

out:
	if (ciphername)
		free(ciphername);
	return ret;
}

static struct sha_backend kcapi_sha =
{
	kcapi_sha_generate,	/* hash_generate */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(kcapi_sha_backend)
static void kcapi_sha_backend(void)
{
	register_sha_impl(&kcapi_sha);
}

/************************************************
 * DRBG cipher interface functions
 ************************************************/

static int kcapi_drbg_generate(struct drbg_data *data, flags_t parsed_flags)
{
#define DRBGNAMELEN 50
	char ciphername[(DRBGNAMELEN + 1)];
	struct buffer tmp;
	struct buffer tmpentropy;
	int ret = 1;

	(void)parsed_flags;

	memset(ciphername, 0, sizeof(ciphername));
	if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA1) {
		if (data->pr) {
			if ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC)
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_pr_hmac_sha1");
			else
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_pr_sha1");
		} else {
			if ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC)
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_nopr_hmac_sha1");
			else
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_nopr_sha1");
		}
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA256) {
		if (data->pr) {
			if ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC)
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_pr_hmac_sha256");
			else
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_pr_sha256");
		} else {
			if ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC)
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_nopr_hmac_sha256");
			else
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_nopr_sha256");
		}
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA384) {
		if (data->pr) {
			if ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC)
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_pr_hmac_sha384");
			else
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_pr_sha384");
		} else {
			if ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC)
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_nopr_hmac_sha384");
			else
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_nopr_sha384");
		}
	} else if ((data->cipher & ACVP_HASHMASK) == ACVP_SHA512) {
		if (data->pr) {
			if ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC)
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_pr_hmac_sha512");
			else
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_pr_sha512");
		} else {
			if ((data->type & ACVP_DRBGMASK) == ACVP_DRBGHMAC)
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_nopr_hmac_sha512");
			else
				snprintf(ciphername, DRBGNAMELEN,
					 "drbg_nopr_sha512");
		}
	} else if ((data->cipher & ACVP_AESMASK) == ACVP_AES128) {
		if (data->pr)
			snprintf(ciphername, DRBGNAMELEN,
				 "drbg_pr_ctr_aes128");
		else
			snprintf(ciphername, DRBGNAMELEN,
				 "drbg_nopr_ctr_aes128");

	} else if ((data->cipher & ACVP_AESMASK) == ACVP_AES192) {
		if (data->pr)
			snprintf(ciphername, DRBGNAMELEN,
				 "drbg_pr_ctr_aes192");
		else
			snprintf(ciphername, DRBGNAMELEN,
				 "drbg_nopr_ctr_aes192");
	} else if ((data->cipher & ACVP_AESMASK) == ACVP_AES256) {
		if (data->pr)
			snprintf(ciphername, DRBGNAMELEN,
				 "drbg_pr_ctr_aes256");
		else
			snprintf(ciphername, DRBGNAMELEN,
				 "drbg_nopr_ctr_aes256");
	} else {
		logger(LOGGER_WARN, "DRBG with unhandled cipher detected\n");
		return -EFAULT;
	}

	tmp.buf = (uint8_t *)ciphername;
	tmp.len = strlen(ciphername);
	CKINT(kcapi_writedata("name", &tmp));
	logger(LOGGER_VERBOSE, "name = %s\n", ciphername);

	CKINT(kcapi_writeu32("type", DRBG));
	logger(LOGGER_VERBOSE, "type = %u\n", DRBG);

	/* concatenate entropy and nonce */
	memset(&tmpentropy, 0, sizeof(struct buffer));
	CKINT(alloc_buf(data->entropy.len + data->nonce.len, &tmpentropy));
	memcpy(tmpentropy.buf, data->entropy.buf, data->entropy.len);
	memcpy(tmpentropy.buf + data->entropy.len, data->nonce.buf,
	       data->nonce.len);
	free_buf(&data->entropy);
	copy_ptr_buf(&data->entropy, &tmpentropy);
	CKINT(kcapi_writedata("drbg_entropy", &data->entropy));
	logger_binary(LOGGER_DEBUG, data->entropy.buf, data->entropy.len,
		      "entropy string written");

	CKINT(kcapi_writedata("drbg_pers", &data->pers));
	logger_binary(LOGGER_DEBUG, data->pers.buf, data->pers.len,
		      "personalization string written");

	CKINT(kcapi_writedata("drbg_addtla", &data->addtl_generate.buffers[0]));
	logger_binary(LOGGER_DEBUG, data->addtl_generate.buffers[0].buf,
		      data->addtl_generate.buffers[0].len,
		      "additional data A written");

	CKINT(kcapi_writedata("drbg_addtlb", &data->addtl_generate.buffers[1]));
	logger_binary(LOGGER_DEBUG, data->addtl_generate.buffers[1].buf,
		      data->addtl_generate.buffers[1].len,
		      "additional data B written");

	CKINT(kcapi_writedata("drbg_entpra",
			      &data->entropy_generate.buffers[0]));
	logger_binary(LOGGER_DEBUG, data->entropy_generate.buffers[0].buf,
		      data->entropy_generate.buffers[0].len,
		      "entropy PR data A written");

	CKINT(kcapi_writedata("drbg_entprb",
			      &data->entropy_generate.buffers[1]));
	logger_binary(LOGGER_DEBUG, data->entropy_generate.buffers[1].buf,
		      data->entropy_generate.buffers[1].len,
		      "entropy PR data B written");

	CKINT(kcapi_writedata("drbg_entropyreseed",
			      &data->entropy_reseed.buffers[0]));
	logger_binary(LOGGER_DEBUG, data->entropy_reseed.buffers[0].buf,
		      data->entropy_reseed.buffers[0].len,
		      "reseed entropy written");

	CKINT(kcapi_writedata("drbg_addtlreseed",
			      &data->addtl_reseed.buffers[0]));
	logger_binary(LOGGER_DEBUG, data->addtl_reseed.buffers[0].buf,
		      data->addtl_reseed.buffers[0].len,
		      "reseed additional data written");

	CKINT(alloc_buf(data->rnd_data_bits_len / 8, &data->random));

	CKINT(kcapi_readdata("data", &data->random));
	logger_binary(LOGGER_DEBUG, data->random.buf, data->random.len,
		      "random data read");

	ret = 0;

out:
	return ret;
}

static struct drbg_backend kcapi_drbg =
{
	kcapi_drbg_generate,	/* drbg_generate */
};

ACVP_DEFINE_CONSTRUCTOR(kcapi_drbg_backend)
static void kcapi_drbg_backend(void)
{
	register_drbg_impl(&kcapi_drbg);
}
