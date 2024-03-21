/* Linux RNG Hash Test Interface
 *
 * Copyright (C) 2020 - 2022, Stephan Mueller <smueller@chronox.de>
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

#include <errno.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include "backend_common.h"

static int lrng_open_fd(const char *path, int *ret_fd)
{
	int fd = *ret_fd;

	if (fd != -1) {
		logger(LOGGER_ERR, "File descriptor already open\n");
		return -EFAULT;
	}

	fd = open(path, O_RDWR);
	if (fd < 0) {
		int errsv = errno;

		logger(LOGGER_ERR, "Cannot open file: %d\n", errsv);
		return -errsv;
	}

	*ret_fd = fd;

	return 0;
}

/************************************************
 * SHA cipher interface functions
 ************************************************/
#define LRNG_SHA_INTERFACE	"/sys/kernel/debug/lrng_testing/lrng_acvt_hash"

static int lrng_sha_fd = -1;
ACVP_DEFINE_CONSTRUCTOR(lrng_sha_open_fd)
static void lrng_sha_open_fd(void)
{
	lrng_open_fd(LRNG_SHA_INTERFACE, &lrng_sha_fd);
}

static int lrng_sha_generate(struct sha_data *data, flags_t parsed_flags)
{
	unsigned int digestlen;
	ssize_t written;
	int ret = 0;

	(void)parsed_flags;

	switch (data->cipher) {
	case ACVP_SHA1:
		digestlen = 20;
		break;
	case ACVP_SHA256:
		digestlen = 32;
		break;
	default:
		logger(LOGGER_ERR, "LRNG only supports SHA-1 or SHA-256\n");
		return -EINVAL;
	}

	CKINT_LOG(alloc_buf(digestlen, &data->mac),
			    "SHA buffer cannot be allocated\n");

	if (lrng_sha_fd < 0) {
		logger(LOGGER_ERR, "SHA file descriptor not open\n");
		return -EFAULT;
	}

	lseek(lrng_sha_fd, 0, SEEK_SET);
	written = write(lrng_sha_fd, data->msg.buf, data->msg.len);
	if (written < 0) {
		ret = -errno;
		logger(LOGGER_ERR, "Cannot write data to kernel: %d\n", ret);
		goto out;

	}
	if (data->msg.len != (size_t)written) {
		logger(LOGGER_ERR,
		       "Write operation incomplete: %zu written, %zu expeted to be written\n",
		       (size_t)written, data->msg.len);
		ret = -EFAULT;
		goto out;
	}

	lseek(lrng_sha_fd, 0, SEEK_SET);
	written = read(lrng_sha_fd, data->mac.buf, data->mac.len);
	if (written < 0) {
		ret = -errno;
		logger(LOGGER_ERR, "Cannot read data from kernel: %d\n",
			ret);
		goto out;
	}
	if (data->mac.len != (size_t)written) {
		logger(LOGGER_ERR,
		       "Read operation incomplete: %zu read, %zu expeted to be read\n",
		       (size_t)written, data->mac.len);
		ret = -EFAULT;
		goto out;
	}

	logger_binary(LOGGER_DEBUG, data->mac.buf, data->mac.len, "hash");

out:
	return ret;
}

static struct sha_backend lrng_sha =
{
	lrng_sha_generate,   /* hash_generate */
	NULL
};

ACVP_DEFINE_CONSTRUCTOR(lrng_sha_backend)
static void lrng_sha_backend(void)
{
	register_sha_impl(&lrng_sha);
}

/************************************************
 * DRBG cipher interface functions
 ************************************************/

#define LRNG_DRNG_INTERFACE	"/sys/kernel/debug/lrng_testing/lrng_acvt_drng"

static int lrng_drng_fd = -1;
ACVP_DEFINE_CONSTRUCTOR(lrng_drng_open_fd)
static void lrng_drng_open_fd(void)
{
	lrng_open_fd(LRNG_DRNG_INTERFACE, &lrng_drng_fd);
}

static int lrng_drbg_generate(struct drbg_data *data, flags_t parsed_flags)
{
	BUFFER_INIT(tmpentropy);
	ssize_t written;
	int ret = 0;

	(void)parsed_flags;

	if (lrng_drng_fd < 0) {
		logger(LOGGER_ERR, "DRNG file descriptor not open\n");
		return -EFAULT;
	}

	/* concatenate entropy and nonce */
	CKINT(alloc_buf(data->entropy.len + data->nonce.len, &tmpentropy));
	memcpy(tmpentropy.buf, data->entropy.buf, data->entropy.len);
	memcpy(tmpentropy.buf + data->entropy.len, data->nonce.buf,
	       data->nonce.len);

	lseek(lrng_drng_fd, 0, SEEK_SET);
	written = write(lrng_drng_fd, tmpentropy.buf, tmpentropy.len);
	if (written < 0) {
		ret = -errno;
		logger(LOGGER_ERR, "Cannot write data to kernel: %d\n", ret);
		goto out;

	}
	if (tmpentropy.len != (size_t)written) {
		logger(LOGGER_ERR,
		       "Write operation incomplete: %zu written, %zu expeted to be written\n",
		       (size_t)written, tmpentropy.len);
		ret = -EFAULT;
		goto out;
	}

	CKINT(alloc_buf(data->rnd_data_bits_len / 8, &data->random));

	lseek(lrng_drng_fd, 0, SEEK_SET);
	written = read(lrng_drng_fd, data->random.buf, data->random.len);
	if (written < 0) {
		ret = -errno;
		logger(LOGGER_ERR, "Cannot read data from kernel: %d\n",
			ret);
		goto out;
	}
	if (data->random.len != (size_t)written) {
		logger(LOGGER_ERR,
		       "Read operation incomplete: %zu read, %zu expeted to be read\n",
		       (size_t)written, data->random.len);
		ret = -EFAULT;
		goto out;
	}

out:
	free_buf(&tmpentropy);
	return ret;
}

static struct drbg_backend lrng_drbg =
{
	lrng_drbg_generate,	/* drbg_generate */
};

ACVP_DEFINE_CONSTRUCTOR(lrng_drbg_backend)
static void lrng_drbg_backend(void)
{
	register_drbg_impl(&lrng_drbg);
}
