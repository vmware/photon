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

#define SHADOW_JENT_MEMORY_SIZE						\
	(CONFIG_CRYPTO_JITTERENTROPY_MEMORY_BLOCKS *			\
	CONFIG_CRYPTO_JITTERENTROPY_MEMORY_BLOCKSIZE)

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

/*
 * Local copy of struct rand_data from
 * photon-jitterentropy-v6.12/jitterentropy.c.
 *
 * struct rand_data is private to jitterentropy.c
 * this wrapper has to reach ec->pmem and ec->mem in
 * order to make the mem blockbuffer reachable from the free path. See
 * jcw_kzalloc() below.
 *
 * The member list is duplicated in full, so the layout is identical and
 * sizeof() identifies an entropy-collector allocation exactly.
 *
 * This is a necessary hack to fix the entropy collector free path.
 * If jitterentropy code ever changes, this particular copy also needs to
 * be updated accordingly along with jitterentropy.
 */
#define SHADOW_JENT_LAG_HISTORY_SIZE 8

enum shadow_jcw_gcd_state_t {
	SHADOW_GCD_NOT_INITIALIZED = 0,
	SHADOW_GCD_INITIALIZED,
	SHADOW_GCD_READY,
};

struct shadow_jcw_rand_data {
	void *hash_state;
	__u64 prev_time;
	__u64 last_delta;
	__s64 last_delta2;
	unsigned int flags;
	unsigned int osr;
	unsigned char *pmem;
	unsigned char *mem;
	unsigned int memlocation;
	unsigned int memblocks;
	unsigned int memblocksize;
	unsigned int memaccessloops;
	unsigned int rct_count;
	unsigned int apt_cutoff;
	unsigned int apt_cutoff_permanent;
	unsigned int apt_observations;
	unsigned int apt_count;
	unsigned int apt_base;
	unsigned int health_failure;
	unsigned int apt_base_set:1;
	unsigned int lag_global_cutoff;
	unsigned int lag_local_cutoff;
	unsigned int lag_prediction_success_count;
	unsigned int lag_prediction_success_run;
	unsigned int lag_best_predictor;
	unsigned int lag_observations;
	__u64 lag_delta_history[SHADOW_JENT_LAG_HISTORY_SIZE];
	unsigned int lag_scoreboard[SHADOW_JENT_LAG_HISTORY_SIZE];
	__u64 gcd;
	enum shadow_jcw_gcd_state_t gcd_state;
};

void *jcw_kzalloc(size_t size)
{
	struct shadow_jcw_rand_data *ec;

	/*
	 * jent_entropy_collector_alloc() is the only caller of jcw_kzalloc() in
	 * jitterentropy.c, and it allocates exactly one struct rand_data. Point
	 * ->pmem at ->mem for that allocation so the noise buffer becomes
	 * reachable from jent_entropy_collector_free().
	 *
	 * The passed size should exactly match the size of shadow rand_data.
	 * If it doesn't match, the structure has drifted and should fail.
	 */
	BUG_ON(size != sizeof(struct shadow_jcw_rand_data));

	ec = kzalloc(size, GFP_KERNEL);
	if (!ec)
		return NULL;

	ec->pmem = (unsigned char *)&ec->mem;

	return ec;
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

	ptr = kvzalloc(algn_len, GFP_KERNEL);
	if (IS_ERR_OR_NULL(ptr)) {
		pr_err("\n Failed to allocate aligned memory");
		return NULL;
	}

	return (unsigned char *)PAGE_ALIGN((unsigned long)ptr);
}

/*
 * @ptr is ec->pmem, i.e. the address of the collector's ->mem member rather
 * than the buffer itself - see jcw_kzalloc(). Load the buffer from it, restore
 * write-back on the pages that jent_entropy_collector_alloc() mapped as
 * uncacheable, and release it.
 */
void jcw_kvzfree(void *ptr, unsigned int len)
{
	unsigned char *mem = *(unsigned char **)ptr;
	int ret;

	if (!mem)
		return;

	/*
	 * jcw_kvzalloc_align() only ever returns page-aligned memory for a
	 * request of a page or more, so a mem that is not page aligned means
	 * the shadow structure above has drifted from the real
	 * struct rand_data and we are reading the wrong member.
	 */
	BUG_ON(!PAGE_ALIGNED(mem) || len != SHADOW_JENT_MEMORY_SIZE);

	/*
	 * Undo the jcw_set_memory_uc() done at alloc time before the pages go
	 * back to the page allocator.
	 */
	ret = set_memory_wb((unsigned long)mem, len >> JENT_PAGE_SHIFT);
	WARN(ret < 0, "Failed to set jent mem to write back 0x%p: %d\n",
							(void *)mem, ret);

	kvfree(mem);
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
