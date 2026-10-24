/*
 * Kernel APIs wrapper for jitterentropy v3.4.1.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */

#include <linux/string.h>
#include <linux/cacheinfo.h>
#include <linux/mutex.h>
#include <linux/vmalloc.h>
#include <linux/slab.h>
#include <linux/fips.h>
#include "jitterentropy.h"

void *jcw_mutex_init(void)
{
	struct mutex *m = kzalloc(sizeof(struct mutex), GFP_KERNEL);
	if (m)
		mutex_init(m);

	return (void *)m;
}

void jcw_mutex_lock(void *m)
{
	mutex_lock((struct mutex *)m);
}

void jcw_mutex_unlock(void *m)
{
	mutex_unlock((struct mutex *)m);
}

void *jcw_kzalloc(size_t size)
{
	return vzalloc(size);
}

void *jcw_memcpy(void *dst, const void *src, size_t len)
{
	return memcpy(dst, src, len);
}

void jcw_memzero_explicit(void *s, size_t count)
{
	return memzero_explicit(s, count);
}

unsigned int jcw_cache_size_roundup(void)
{
	unsigned int i = 0, size = 0;
	struct cpu_cacheinfo *info_ci = get_cpu_cacheinfo(0);
	struct cacheinfo *info = NULL;

	for (i = 0; i< info_ci->num_leaves; i++) {
		info = info_ci->info_list + i;
		size += info->size;
	}

	/* Force the output_size to be of the form (bounding_pwr_of_2 - 1)*/
	size |= (size >> 1);
	size |= (size >> 2);
	size |= (size >> 4);
	size |= (size >> 8);
	size |= (size >> 16);

	if (size == 0)
		return 0;

	/* Make the output_size the smallest power of 2 strictly greater than
		cache_size. */
	size++;
	return size;
}

int jcw_fips_enabled(void)
{
	return fips_enabled;
}

void jcw_zfree(void *ptr, unsigned int len)
{
	memzero_explicit(ptr, len);
	vfree(ptr);
}

u64 jcw_ktime_get_ns(void)
{
	return ktime_get_ns();
}

unsigned long jcw_random_get_entropy(void)
{
	return random_get_entropy();
}
