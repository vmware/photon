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

#include <stdint.h>

#ifndef _CONVERSION_BE_LE_H
#define _CONVERSION_BE_LE_H

#ifdef __cplusplus
extern "C"
{
#endif

#undef TEST

#define GCC_VERSION (__GNUC__ * 10000		\
		     + __GNUC_MINOR__ * 100	\
		     + __GNUC_PATCHLEVEL__)
#if !defined(TEST) && (GCC_VERSION >= 40400 || defined(__clang__))
# define __HAVE_BUILTIN_BSWAP16__
# define __HAVE_BUILTIN_BSWAP32__
# define __HAVE_BUILTIN_BSWAP64__
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

#if !defined(__HAVE_BUILTIN_BSWAP32__) || !defined(__HAVE_BUILTIN_BSWAP64__)
static inline uint32_t rol(uint32_t x, int n)
{
	return ( (x << (n&(32-1))) | (x >> ((32-n)&(32-1))) );
}

static inline uint32_t ror(uint32_t x, int n)
{
	return ( (x >> (n&(32-1))) | (x << ((32-n)&(32-1))) );
}

static inline uint32_t _bswap32(uint32_t x)
{
	return ((rol(x, 8) & 0x00ff00ffL) | (ror(x, 8) & 0xff00ff00L));
}
# define _swap32(x) _bswap32(x)
#else
# define _swap32(x) (uint32_t)__builtin_bswap32((uint32_t)(x))
#endif

#ifndef __HAVE_BUILTIN_BSWAP64__
static inline uint64_t _bswap64(uint64_t x)
{
	return ((uint64_t)_bswap32(x) << 32) | (_bswap32(x >> 32));
}
# define _swap64(x) _bswap64(x)
#else
# define _swap64(x) (uint64_t)__builtin_bswap64((uint64_t)(x))
#endif

/* Endian dependent byte swap operations.  */
/* Endian dependent byte swap operations.  */
#if __BYTE_ORDER__ ==  __ORDER_BIG_ENDIAN__
# define le_bswap16(x) _swap16(x)
# define be_bswap16(x) ((uint16_t)(x))
# define le_bswap32(x) _swap32(x)
# define be_bswap32(x) ((uint32_t)(x))
# define le_bswap64(x) _swap64(x)
# define be_bswap64(x) ((uint64_t)(x))
#elif __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
# define le_bswap16(x) ((uint16_t)(x))
# define be_bswap16(x) _swap16(x)
# define le_bswap32(x) ((uint32_t)(x))
# define be_bswap32(x) _swap32(x)
# define le_bswap64(x) ((uint64_t)(x))
# define be_bswap64(x) _swap64(x)
#else
# error "Endianess not defined"
#endif

#ifdef TEST
#include <stdio.h>
void compiler_test_le(void)
{
#if GCC_VERSION >= 40400
	uint16_t u16 = 1234;
	uint32_t u32 = 1234567890;
	uint64_t u64 = 1234567890123456789;

	if (_bswap16(u16) != __builtin_bswap16(u16))
		printf("FAIL: compiler swap16 is not consistent with C (compiler %d, C %d)\n", __builtin_bswap16(u16), _bswap16(u16));
	else
		printf("PASS: compiler swap16 consistent with C\n");

	if (_bswap32(u32) != __builtin_bswap32(u32))
		printf("FAIL: compiler swap32 is not consistent with C (compiler %u, C %u)\n", __builtin_bswap32(u32), _bswap32(u32));
	else
		printf("PASS: compiler swap32 consistent with C\n");

	if (_bswap64(u64) != __builtin_bswap64(u64))
		printf("FAIL: compiler swap64 is not consistent with C (compiler %lu, C %lu)\n", __builtin_bswap64(u64), _bswap64(u64));
	else
		printf("PASS: compiler swap64 consistent with C\n");
#else
	printf("DEACT: compiler swap not defined\n");
	return;
#endif
}

void sw_test_le(void)
{
	uint16_t u16 = 1234;
	uint32_t u32 = 1234567890;
	uint64_t u64 = 1234567890123456789;

	if (_bswap16(u16) != be_bswap16(u16))
		printf("FAIL: macro swap16 is not consistent with C (macro %d, C %d)\n", be_bswap16(u16), _bswap16(u16));
	else
		printf("PASS: macro swap16 consistent with C\n");

	if (_bswap32(u32) != be_bswap32(u32))
		printf("FAIL: macro swap32 is not consistent with C (macro %u, C %u)\n", be_bswap32(u32), _bswap32(u32));
	else
		printf("PASS: macro swap32 consistent with C\n");

	if (_bswap64(u64) != be_bswap64(u64))
		printf("FAIL: macro swap64 is not consistent with C (macro %lu, C %lu)\n", be_bswap64(u64), _bswap64(u64));
	else
		printf("PASS: macro swap64 consistent with C\n");
}

int main(void)
{
#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
	compiler_test_le();
	sw_test_le();
#else
# error "no testing defined"
#endif

	return 0;
}
#endif

#ifdef __cplusplus
}
#endif

#endif /* _CONVERSION_BE_LE_H */
