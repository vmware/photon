/*
 * Kernel APIs wrapper for jitterentropy v3.4.1.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */

extern void *jcw_mutex_init(void);
extern void jcw_mutex_lock(void *m);
extern void jcw_mutex_unlock(void *m);
extern unsigned int jcw_cache_size_roundup(void);
extern void *jcw_memcpy(void *dst, const void *src, size_t len);
extern int jcw_printk(const char *fmt, ...);
extern void *jcw_kzalloc(size_t size);
