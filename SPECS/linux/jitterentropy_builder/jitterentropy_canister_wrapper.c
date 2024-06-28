/*
 * Kernel APIs wrapper for jitterentropy v3.4.1.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */

#include <linux/cacheinfo.h>
#include <linux/mutex.h>
#include <linux/slab.h>
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
	return kzalloc(size, GFP_KERNEL);
}

void *jcw_memcpy(void *dst, const void *src, size_t len)
{
	return memcpy(dst, src, len);
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

