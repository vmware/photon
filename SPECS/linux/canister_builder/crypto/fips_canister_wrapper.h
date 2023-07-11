/*
 * Kernel APIs wrapper for the canister.
 *
 * Copyright (C) 2020 - 2022 VMware, Inc.
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
#include <linux/version.h>
#include <linux/workqueue.h>
#include <crypto/aead.h>
#include <crypto/hash.h>
#include <crypto/akcipher.h>
#include <crypto/skcipher.h>
#include <crypto/kpp.h>
#include <linux/uio.h>
#include <crypto/algapi.h>
#include <crypto/sha1_base.h>
#include <crypto/sha512_base.h>

#ifndef CONFIG_GCC_PLUGIN_STACKLEAK
void __used __no_caller_saved_registers noinstr stackleak_track_stack(void);
#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
int _printk(const char *fmt, ...);
#endif

extern u32 fcw_prandom_u32_max(u32 ep_ro);

extern void __noreturn __fcw_module_put_and_kthread_exit(struct module *mod,
			long code);
#define fcw_module_put_and_kthread_exit(code) __fcw_module_put_and_kthread_exit(THIS_MODULE, code)


extern void __init fcw_mem_free(void *p);
extern void * __init fcw_mem_alloc(size_t size);

extern int fcw_cond_resched(void);

extern void *fcw_kmalloc(size_t size, gfp_t flags);
extern void *fcw_kzalloc(size_t size, gfp_t flags);

extern int fcw_signal_pending(void);
extern void *fcw_kthread_run(int (*threadfn)(void *data), void *data, const char namefmt[]);
extern void *fcw_mutex_init(void);
extern void fcw_mutex_lock(void *m);
extern void fcw_mutex_unlock(void *m);

extern bool fcw_schedule_work(struct work_struct *work);
extern size_t fcw_copy_from_iter(void *addr, size_t bytes, struct iov_iter *i);
extern void *fcw_memcpy(void *dst, const void *src, size_t len);
extern int fcw_sha1_base_do_update(struct shash_desc *desc,
				      const u8 *data,
				      unsigned int len,
				      sha1_block_fn *block_fn);
extern int fcw_sha512_base_do_update(struct shash_desc *desc,
					const u8 *data,
					unsigned int len,
					sha512_block_fn *block_fn);
extern size_t fcw_strlcpy(char *dest, const char *src, size_t size);
extern void fcw_bug(void);
extern void fcw_bug_on(int cond);
extern int fcw_warn_on(int cond);
extern int fcw_warn_on_once(int cond);
extern int fcw_warn(int cond, const char *fmt, ...);
extern void fcw_sg_assign_page(struct scatterlist *sg, struct page *page);
extern void fcw_sg_set_buf(struct scatterlist *sg, const void *buf,
			      unsigned int buflen);
extern void *fcw_sg_virt(struct scatterlist *sg);
extern void *fcw_scatterwalk_map(struct scatter_walk *walk);
extern int fcw_printk(const char *fmt, ...);

extern bool fcw_ratelimit(void *rs, const char *name);
extern void *fcw_init_ratelimit_state(void *rs);

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

