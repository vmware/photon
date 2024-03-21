/*
 * Copyright (C) 2020 - 2022, Stephan Mueller <smueller@chronox.de>
 *
 * License: see LICENSE file in root directory
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

/*
 * The following functions are helper functions to implement
 * the SHA1/2, SHA3 and SHAKE MCT inner loop.
 */

#ifndef PARSER_SHA_MCT_HELPER_H
#define PARSER_SHA_MCT_HELPER_H

#include "logger.h"
#include "parser_cshake.h"
#include "parser_sha.h"
#include "stringhelper.h"

#ifdef __cplusplus
extern "C"
{
#endif

static inline int sha_ldt_helper(struct sha_data *data, struct buffer *msg_p)
{
	int ret = 0;

	if (data->ldt_expansion_size) {
		size_t i, len = data->msg.len;

		if (SIZE_MAX < data->ldt_expansion_size / 8) {
			logger(LOGGER_ERR, "LDT size not supported on IUT\n");
			return -EINVAL;
		}

		CKINT(alloc_buf(data->ldt_expansion_size / 8, msg_p));
		for (i = 0; i < msg_p->len; i += len) {
			len = (data->ldt_expansion_size - i) < data->msg.len ?
			      (data->ldt_expansion_size - i) : data->msg.len;

			memcpy(msg_p->buf + i, data->msg.buf, len);
		}
	} else {
		msg_p->buf = data->msg.buf;
		msg_p->len = data->msg.len;
	}

out:
	return ret;
}

static inline void sha_ldt_clear_buf(struct sha_data *data,
				     struct buffer *msg_p)
{
	if (data->ldt_expansion_size)
		free_buf(msg_p);
}

/**
 * @brief SHA-1 and SHA-2 Monte-Carlo Testing inner loop implementation.
 *
 * This is a service function that may be used when implementing the MCT
 * inner loop. To utilize the function, the data provided by the parser
 * needs to be provided and a function call back implementing one hash
 * operation.
 *
 * An example of how to use it is given with
 * backend_openssl.c:openssl_hash_inner_loop
 */
static inline int
parser_sha2_inner_loop(struct sha_data *data, flags_t parsed_flags,
		       int (*hash_generate)(struct sha_data *data,
					    flags_t parsed_flags))
{
	unsigned int j;
	int ret;

	if (!hash_generate)
		return -EOPNOTSUPP;

	for (j = 0; j < 1000; j++) {
		unsigned int k = 0;

		free_buf(&data->mac);
		CKINT_LOG(hash_generate(data, parsed_flags),
			  "SHA operation failed\n");

		/* move the two last blocks to the front */
		for (k = 0; k < data->mac.len * 2; k++)
			data->msg.buf[k] =
				data->msg.buf[(k + data->mac.len)];
		/* place newly calculated message to the end */
		memcpy(data->msg.buf + data->mac.len * 2,
		       data->mac.buf, data->mac.len);
	}

out:
	return ret;
}

/**
 * @brief SHA-3 Monte-Carlo Testing inner loop implementation.
 *
 * This is a service function that may be used when implementing the MCT
 * inner loop. To utilize the function, the data provided by the parser
 * needs to be provided and a function call back implementing one hash
 * operation.
 *
 * An example of how to use it is given with
 * backend_openssl.c:openssl_hash_inner_loop
 */
static inline int
parser_sha3_inner_loop(struct sha_data *data, flags_t parsed_flags,
		       int (*hash_generate)(struct sha_data *data,
					    flags_t parsed_flags))
{
	unsigned int j;
	int ret;

	if (!hash_generate)
		return -EOPNOTSUPP;

	for (j = 0; j < 1000; j++) {
		free_buf(&data->mac);
		CKINT_LOG(hash_generate(data, parsed_flags),
			  "SHA operation failed\n");

		/* hash becomes new message */
		memcpy(data->msg.buf, data->mac.buf, data->mac.len);
	}

out:
	return ret;
}

#define min(x, y)	(((size_t)x < (size_t)y) ? x : y)

#define GCC_VERSION (__GNUC__ * 10000		\
		     + __GNUC_MINOR__ * 100	\
		     + __GNUC_PATCHLEVEL__)
#if !defined(TEST) && (GCC_VERSION >= 40400 || defined(__clang__))
# define __HAVE_BUILTIN_BSWAP16__
#endif

/****************
 * Rotate the 32 bit unsigned integer X by N bits left/right
 */
/* Byte swap for 16-bit, 32-bit and 64-bit integers. */
#ifndef __HAVE_BUILTIN_BSWAP16__
static inline uint16_t rol16(uint16_t x, int n)
{
	return ( (x << (n&(16-1))) | (x >> ((16-n)&(16-1))) );
}

static inline uint16_t ror16(uint16_t x, int n)
{
	return ( (x >> (n&(16-1))) | (x << ((16-n)&(16-1))) );
}

static inline uint16_t _bswap16(uint16_t x)
{
	return ((rol16(x, 8) & 0x00ff) | (ror16(x, 8) & 0xff00));
}
# define _swap16(x) _bswap16(x)
#else
# define _swap16(x) (uint16_t)__builtin_bswap16((uint16_t)(x))
#endif

/* Endian dependent byte swap operations.  */
/* Endian dependent byte swap operations.  */
#if __BYTE_ORDER__ ==  __ORDER_BIG_ENDIAN__
# define be_bswap16(x) ((uint16_t)(x))
#elif __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
# define be_bswap16(x) _swap16(x)
#else
# error "Endianess not defined"
#endif

/**
 * @brief SHAKE Monte-Carlo Testing inner loop implementation.
 *
 * This is a service function that may be used when implementing the MCT
 * inner loop. To utilize the function, the data provided by the parser
 * needs to be provided and a function call back implementing one hash
 * operation.
 *
 * An example of how to use it is given with
 * backend_openssl.c:openssl_hash_inner_loop
 */
static inline int
parser_shake_inner_loop(struct sha_data *data, flags_t parsed_flags,
			int (*hash_generate)(struct sha_data *data,
					     flags_t parsed_flags))
{
	uint32_t minoutbytes = (data->minoutlen + 7) / 8,
		 maxoutbytes = data->maxoutlen / 8;
	size_t read_outbits;
	uint32_t range = maxoutbytes - minoutbytes + 1;
	uint16_t outbits = 0;
	unsigned int j;
	int ret;

	if (!hash_generate)
		return -EOPNOTSUPP;

	CKNULL(minoutbytes, -EOPNOTSUPP);
	CKNULL(maxoutbytes, -EOPNOTSUPP);

	for (j = 0; j < 1000; j++) {
		free_buf(&data->mac);
		CKINT_LOG(hash_generate(data, parsed_flags),
			  "SHAKE operation failed\n");

		/* hash becomes new message */
		memset(data->msg.buf, 0, data->msg.len);
		memcpy(data->msg.buf, data->mac.buf,
			min(data->msg.len, data->mac.len));

		read_outbits = min(data->mac.len, sizeof(outbits));

		/*
		 * Rightmost_Output_bits = rightmost 16 bits of
		 * Output_i.
		 */
		memcpy(&outbits + sizeof(outbits) - read_outbits,
			data->mac.buf + data->mac.len - read_outbits,
			read_outbits);

		/* Convert read value into an integer */
		outbits = be_bswap16(outbits);

		data->outlen = minoutbytes + (outbits % range);
		data->outlen *= 8;
	}

out:
	return ret;
}


/**
 * @brief cSHAKE Monte-Carlo Testing inner loop implementation.
 *
 * This is a service function that may be used when implementing the MCT
 * inner loop. To utilize the function, the data provided by the parser
 * needs to be provided and a function call back implementing one hash
 * operation.
 *
 * An example of how to use it is given with
 * backend_openssl.c:openssl_hash_inner_loop
 */
static inline int
parser_cshake_inner_loop(struct cshake_data *data, flags_t parsed_flags,
			 int (*cshake_generate)(struct cshake_data *data,
					        flags_t parsed_flags))
{
	uint32_t minoutbits = data->minoutlen,
		 maxoutbits = data->maxoutlen;
	size_t read_outbits;
	uint32_t range = maxoutbits - minoutbits + 1;
	uint16_t outbits = 0;
	unsigned int j;
	int ret;

	if (!cshake_generate)
		return -EOPNOTSUPP;

	CKNULL(minoutbits, -EOPNOTSUPP);
	CKNULL(maxoutbits, -EOPNOTSUPP);

	for (j = 0; j < 1000; j++) {
		size_t new_cust_len;

		free_buf(&data->mac);
		CKINT_LOG(cshake_generate(data, parsed_flags),
			  "cSHAKE operation failed\n");

		read_outbits = min(data->mac.len, sizeof(outbits));

		/*
		 * Rightmost_Output_bits = rightmost 16 bits of
		 * Output_i.
		 */
		memcpy(&outbits + sizeof(outbits) - read_outbits,
		       data->mac.buf + data->mac.len - read_outbits,
		       read_outbits);

		/* Convert read value into an integer */
		outbits = be_bswap16(outbits);

		/* New customization string */
		memset(data->customization.buf, 0, data->customization.len);
		new_cust_len = data->msg.len + sizeof(outbits);
		free_buf(&data->customization);
		CKINT_LOG(alloc_buf(new_cust_len, &data->customization),
			  "Cannot allocate customization buffer\n");
		memcpy(data->customization.buf, data->msg.buf, data->msg.len);
		memcpy(data->customization.buf + data->msg.len, &outbits,
		       sizeof(outbits));

		/* hash becomes new message */
		memset(data->msg.buf, 0, data->msg.len);
		memcpy(data->msg.buf, data->mac.buf,
			min(data->msg.len, data->mac.len));

		//TODO outlenincrement
		data->outlen = minoutbits + ((outbits % range) / 8) * 8;
	}

out:
	return ret;
}

#undef min
#undef GCC_VERSION
#undef be_bswap16

#ifdef __cplusplus
}
#endif

#endif /* PARSER_SHA_MCT_HELPER_H */
