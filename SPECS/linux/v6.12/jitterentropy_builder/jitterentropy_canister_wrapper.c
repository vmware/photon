/*
 * Kernel APIs wrapper for jitterentropy v3.4.1.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */

#include <linux/string.h>
#include <linux/stdarg.h>
#include <linux/slab.h>
#include <linux/fips.h>
#include <linux/kern_levels.h>
#include <linux/mm.h>
#include <linux/vmalloc.h>
#include <linux/err.h>
#include <asm/set_memory.h>
#include "jitterentropy_canister_wrapper.h"
#include "jitterentropy.h"

/* Prototype definitions */
int jcw_strncasecmp(const char *s1, const char *s2, size_t len);
void *jcw_memcpy(void *dst, const void *src, size_t len);
void jcw_memzero_explicit(void *s, size_t count);
int jcw_printk(const char *fmt, ...);
void *jcw_kzalloc(size_t size);
void *jcw_vzalloc(size_t size);
void *jcw_kvzalloc(unsigned int len);
void *jcw_kvzalloc_align(unsigned char *ptr, unsigned int len);
void jcw_zfree(void *ptr, unsigned int len);
void jcw_kvzfree(void *ptr, unsigned int len);
void jcw_vfree(void *ptr, unsigned int len);
int jcw_set_memory_uc(unsigned char *addr, int numpages);
int jcw_fips_enabled(void);
u64 jcw_ktime_get_ns(void);

inline bool jcw_is_err_or_null(void *ptr);

size_t jcw_strlen(const char *str);
int set_memory_uc(unsigned long addr, int numpages);

inline bool jcw_is_err_or_null(void *ptr)
{
	return IS_ERR_OR_NULL(ptr);
}

void *jcw_kzalloc(size_t size)
{
	return kzalloc(size, GFP_KERNEL);
}

void *jcw_memcpy(void *dst, const void *src, size_t len)
{
	return memcpy(dst, src, len);
}

void jcw_memzero_explicit(void *s, size_t count)
{
	return memzero_explicit(s, count);
}

void *jcw_kvzalloc(unsigned int len)
{
        return kvzalloc(len, GFP_KERNEL);
}

void *jcw_kvzalloc_align(unsigned char *ptr, unsigned int len)
{
	unsigned long algn_len = len;

	if (len < PAGE_SIZE)
		return kvzalloc(len, GFP_KERNEL);

	if (len & ~PAGE_MASK)
		algn_len = roundup(len, PAGE_SIZE);

	ptr = kvzalloc(algn_len + PAGE_SIZE, GFP_KERNEL);
	if (IS_ERR_OR_NULL(ptr)) {
		pr_err("\n Failed to allocate aligned memory");
		return NULL;
	}

	return (unsigned char *)PAGE_ALIGN((unsigned long)ptr);
}

void jcw_kvzfree(void *ptr, unsigned int len)
{
	memzero_explicit(ptr, len);
        kvfree_sensitive(ptr, len);
}

void *jcw_vzalloc(size_t size)
{
	return vzalloc(size);
}

void jcw_vfree(void *ptr, unsigned int len)
{
	memzero_explicit(ptr, len);
	vfree(ptr);
}

int jcw_strncasecmp(const char *s1, const char *s2, size_t len)
{
	return strncasecmp((const char *)s1, (const char *)s2, len);
}

size_t jcw_strlen(const char *str)
{
	return strlen((const char *)str);
}

int jcw_set_memory_uc(unsigned char *addr, int numpages)
{
	return set_memory_uc((unsigned long)addr, numpages);
}

int jcw_fips_enabled(void)
{
	return fips_enabled;
}

void jcw_zfree(void *ptr, unsigned int len)
{
	memzero_explicit(ptr, len);
	kfree_sensitive(ptr);
}

u64 jcw_ktime_get_ns(void)
{
	return ktime_get_ns();
}
