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

#define _DEFAULT_SOURCE
#include <ctype.h>
#include <limits.h>
#include <stdlib.h>

#include "logger.h"
#include "stringhelper.h"


char* get_val(char *str, const char *delim)
{
	char *ret = NULL;
	char *tmp = NULL;
	char *saveptr = NULL;

	ret = strtok_r(str, delim, &saveptr);
	if (!ret)
		return ret;
	/* get the string after the delimiter */
	ret = strtok_r(NULL, delim, &saveptr);
	if (!ret)
		return ret;

	while (*ret != '\0' && isblank(*ret))
		ret++;

	/* remove trailing \n or \r*/
	tmp = ret;
	tmp += strlen(tmp) - 1;
	while ((*tmp == '\n' || *tmp == '\r' || *tmp == ']' ||
		isblank(*tmp)) && tmp >= ret) {
		*tmp = '\0';
		tmp--;
	}

	return ret;
}

static int _get_intval(char *str, const char *delim, uint32_t *val, int base)
{
	char *valstr = NULL;
	size_t vallen = 0;
	unsigned long converted;

	valstr = get_val(str, delim);
	if (!valstr)
		return 1;

	vallen = strlen(valstr);
	while (vallen) {
		if (vallen < 2)
			break;
		if (*valstr == 0 && *(valstr + 1) == 0) {
			vallen -= 2;
			valstr += 2;
		} else
			break;
	}

	converted = strtoul(valstr, NULL, base);
	if (converted > UINT_MAX)
		return -EINVAL;

	*val = (uint32_t)converted;

	return 0;
}

int get_intval(char *str, const char *delim, uint32_t *val)
{
	return _get_intval(str, delim, val, 10);
}

int get_hexval(char *str, const char *delim, uint32_t *val)
{
	return _get_intval(str, delim, val, 16);
}

int get_binval(char *str, const char *delim, struct buffer *buf)
{
	char *hex = NULL;

	if (buf->buf || buf->len) {
		printf("Buffer not empty, refusing to allocate new!\n");
		return -EINVAL;
	}

	hex = get_val(str, delim);
	if (!hex)
		return -EINVAL;

	if (strlen(hex))
		return hex2bin_alloc(hex, (uint32_t)strlen(hex), &buf->buf,
				     &buf->len);
	return 0;
}

void free_buf(struct buffer *buf)
{
	if (!buf)
		return;
	if (buf->buf) {
		free(buf->buf);
		buf->buf = NULL;
	}
	if (buf->len)
		buf->len = 0;
}

int alloc_buf(size_t size, struct buffer *buf)
{
	if (buf->buf) {
		logger(LOGGER_WARN, "Allocate an already allocated buffer!\n");
		return -EFAULT;
	}
	if (!size)
		return 0;

	buf->buf = calloc(1, size);
	if (!buf->buf)
		return -ENOMEM;

	buf->len = size;

	return 0;
}

void copy_ptr_buf(struct buffer *dst, struct buffer *src)
{
	dst->buf = src->buf;
	dst->len = src->len;
}

int left_pad_buf(struct buffer *buf, size_t required_len)
{
	int ret = 0;

	if (buf->len < required_len) {
		struct buffer cpy_tmp;
		BUFFER_INIT(tmp);

		CKINT(alloc_buf(required_len, &tmp));

		if (!tmp.buf)
			goto out;

		memcpy(tmp.buf + required_len - buf->len, buf->buf, buf->len);
		copy_ptr_buf(&cpy_tmp, buf);
		copy_ptr_buf(buf, &tmp);
		free_buf(&cpy_tmp);
	}
out:
	return ret;
}

int remove_leading_zeroes(struct buffer *buf)
{
	int ret = 0;
	size_t i = 0, required_len = buf->len;

	if (!buf->len)
		return ret;

	while (buf->buf[i++] == 0)
		required_len--;
	/* The test above increments i one extra time, we bring it back */
	i--;

	if (buf->len > required_len) {
		struct buffer cpy_tmp;
		BUFFER_INIT(tmp);

		CKINT(alloc_buf(required_len, &tmp));

		if (!tmp.buf)
			goto out;

		memcpy(tmp.buf, buf->buf + i, required_len);
		copy_ptr_buf(&cpy_tmp, buf);
		copy_ptr_buf(buf, &tmp);
		free_buf(&cpy_tmp);
	}
out:
	return ret;
}

int mpi_remove_pad(struct buffer *buf, size_t required_len)
{
	int ret = 0;

	if (buf->len > required_len) {
		struct buffer cpy_tmp;
		BUFFER_INIT(tmp);

		CKINT(alloc_buf(required_len, &tmp));

		if (!tmp.buf)
			goto out;

		memcpy(tmp.buf, buf->buf +  buf->len - required_len,
		       required_len);
		copy_ptr_buf(&cpy_tmp, buf);
		copy_ptr_buf(buf, &tmp);
		free_buf(&cpy_tmp);
	}
out:
	return ret;
}
