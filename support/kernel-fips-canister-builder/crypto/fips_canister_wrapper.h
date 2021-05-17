/*
 * Kernel APIs wrapper for the canister.
 *
 * Copyright (C) 2020, 2021, VMware, Inc.
 * Author: Alexey Makhalov <amakhalov@vmware.com>
 *
 */

#ifndef _FIPS_CANISTER_WRAPPER_H
#define _FIPS_CANISTER_WRAPPER_H

#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/gfp.h>
#include <linux/slab.h>
#include <linux/mutex.h>
#include <linux/sched.h>
#include <linux/workqueue.h>
#include <crypto/aead.h>
#include <crypto/hash.h>
#include <crypto/akcipher.h>
#include <crypto/skcipher.h>
#include <crypto/kpp.h>

extern int fcw_cond_resched(void);

extern void *fcw_kmalloc(size_t size, gfp_t flags);
extern void *fcw_kzalloc(size_t size, gfp_t flags);

extern void *fcw_mutex_init(void);
extern void fcw_mutex_lock(void *m);
extern void fcw_mutex_unlock(void *m);

extern bool fcw_schedule_work(struct work_struct *work);

/* testmgr alloc helpers */
extern struct aead_request *fcw_aead_request_alloc(
	struct crypto_aead *tfm, gfp_t gfp);
extern struct ahash_request *fcw_ahash_request_alloc(
	struct crypto_ahash *tfm, gfp_t gfp);
extern struct akcipher_request *fcw_akcipher_request_alloc(
	struct crypto_akcipher *tfm, gfp_t gfp);
extern struct skcipher_request *fcw_skcipher_request_alloc(
	struct crypto_skcipher *tfm, gfp_t gfp);
extern struct kpp_request *fcw_kpp_request_alloc(
	struct crypto_kpp *tfm, gfp_t gfp);
#endif

