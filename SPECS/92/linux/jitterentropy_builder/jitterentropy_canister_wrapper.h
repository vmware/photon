/*
 * Kernel APIs wrapper for jitterentropy v3.4.1.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */

#ifndef JITTERENTROPY_CANISTER_WRAPPER_H
#define JITTERENTROPY_CANISTER_WRAPPER_H

#include <linux/stddef.h>
#include <linux/build_bug.h>

#define JENT_PAGE_SHIFT 12

extern int jcw_strncasecmp(const char *s1, const char *s2, size_t len);
extern void *jcw_memcpy(void *dst, const void *src, size_t len);
extern void jcw_memzero_explicit(void *s, size_t count);
extern int jcw_printk(const char *fmt, ...);
extern void *jcw_kzalloc(size_t size);
extern void *jcw_kvzalloc(unsigned int len);
extern void *jcw_kvzalloc_align(unsigned char *ptr, unsigned int len);
extern void jcw_zfree(void *ptr, unsigned int len);
extern void jcw_kvzfree(void *ptr, unsigned int len);
extern int jcw_fips_enabled(void);
extern u64 jcw_ktime_get_ns(void);
extern unsigned long jcw_random_get_entropy(void);
extern inline void jcw_pr_info(const char *fmt, ...);
extern inline void jcw_pr_err(const char *fmt, ...);
extern inline bool jcw_is_err_or_null(void *ptr);
extern size_t jcw_strlen(const char *str);
int jcw_set_memory_uc(unsigned char *addr, int numpages);

bool is_jent_mem_access_method_random(void);

#endif
