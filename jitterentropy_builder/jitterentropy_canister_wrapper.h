/*
 * Kernel APIs wrapper for jitterentropy v3.4.1.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */

#ifndef JITTERENTROPY_CANISTER_WRAPPER_H
#define JITTERENTROPY_CANISTER_WRAPPER_H

extern void *jcw_mutex_init(void);
extern void jcw_mutex_lock(void *m);
extern void jcw_mutex_unlock(void *m);
extern unsigned int jcw_cache_size_roundup(void);
extern void *jcw_memcpy(void *dst, const void *src, size_t len);
extern void jcw_memzero_explicit(void *s, size_t count);
extern int jcw_printk(const char *fmt, ...);
extern void *jcw_kzalloc(size_t size);
extern void jcw_zfree(void *ptr, unsigned int len);
extern int jcw_fips_enabled(void);
extern u64 jcw_ktime_get_ns(void);
extern unsigned long jcw_random_get_entropy(void);

#endif
