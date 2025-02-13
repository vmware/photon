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

#undef DEFINE_LOCK_GUARD_1_COND

#ifndef CONFIG_FUNCTION_TRACER
void __fentry__(void);
#endif

#ifndef CONFIG_GCC_PLUGIN_STACKLEAK
void __used __no_caller_saved_registers noinstr stackleak_track_stack(void);
#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
int _printk(const char *fmt, ...);
#endif

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
extern void *fcw_spin_lock_init(void);
extern void fcw_spin_lock_free(void *lock);

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
extern void fcw_bug(void);
extern void fcw_bug_on(int cond);
extern int fcw_warn_on(bool cond);
extern int fcw_warn_on_once(int cond);
extern void fcw_warn(void);
extern int fcw_is_warn_true(int cond);
extern int fcw_warn_printk(const char *fmt, ...);
extern void fcw_sg_assign_page(struct scatterlist *sg, struct page *page);
extern void fcw_sg_set_buf(struct scatterlist *sg, const void *buf,
			      unsigned int buflen);
extern void *fcw_sg_virt(struct scatterlist *sg);
extern void *fcw_scatterwalk_map(struct scatter_walk *walk);
extern int fcw_printk(const char *fmt, ...);

extern bool fcw_ratelimit(void *rs, const char *name);
extern void *fcw_init_ratelimit_state(void *rs);
extern void *fcw_sg_page(struct scatterlist *sg);
extern void fcw_sg_set_page(struct scatterlist *sg, void *page,
			    unsigned int len, unsigned int offset);
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

extern void fcw_scatterwalk_pagedone(struct scatter_walk *walk, int out,
				     unsigned int more);
extern bool fcw_need_resched(void);
extern void *fcw_kmap_local_page(void *page);
extern void fcw_kunmap_local(const void *addr);

int __init rsa_init(void);
void __exit rsa_exit(void);
int __init crypto_cbc_module_init(void);
void __exit crypto_cbc_module_exit(void);
int __init crypto_cmac_module_init(void);
void __exit crypto_cmac_module_exit(void);
int __init sha3_generic_mod_init(void);
void __exit sha3_generic_mod_fini(void);
int __init crypto_ecb_module_init(void);
void __exit crypto_ecb_module_exit(void);
int __init crypto_ctr_module_init(void);
void __exit crypto_ctr_module_exit(void);
int __init ghash_mod_init(void);
void __exit ghash_mod_exit(void);
int __init aes_init(void);
void __exit aes_fini(void);
int __init crypto_self_test_init(void);
int __init ecdsa_init(void);
void __exit ecdsa_exit(void);
int __init sha1_generic_mod_init(void);
void __exit sha1_generic_mod_fini(void);
int __init cryptomgr_init(void);
void __exit cryptomgr_exit(void);
int __init sha512_generic_mod_init(void);
void __exit sha512_generic_mod_fini(void);
int __init crypto_gcm_module_init(void);
void __exit crypto_gcm_module_exit(void);
int __init crypto_ccm_module_init(void);
void __exit crypto_ccm_module_exit(void);
int __init hmac_module_init(void);
void __exit hmac_module_exit(void);
int __init sha256_generic_mod_init(void);
void __exit sha256_generic_mod_fini(void);
int __init xts_module_init(void);
void __exit xts_module_exit(void);
int __init ecdh_init(void);
void __exit ecdh_exit(void);
int __init drbg_init(void);
void __exit drbg_exit(void);
int __init crypto_cts_module_init(void);
void __exit crypto_cts_module_exit(void);
int __init aesni_init(void);
void __exit aesni_exit(void);
int __init fips_integrity_init(void);
int __init fips_integrity_check (void);
int seqiv_module_init(void);
void seqiv_module_exit(void);
int __init echainiv_module_init(void);
void __exit echainiv_module_exit(void);
int __init essiv_module_init(void);
void __exit essiv_module_exit(void);
#endif

