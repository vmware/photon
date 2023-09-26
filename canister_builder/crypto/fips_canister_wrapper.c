/*
 * Kernel APIs wrapper for the canister.
 *
 * Copyright (C) 2020 - 2022 VMware, Inc.
 * Author: Alexey Makhalov <amakhalov@vmware.com>
 *
 */

#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/gfp.h>
#include <linux/slab.h>
#include <linux/mutex.h>
#include <linux/version.h>
#include <linux/printk.h>

#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
#include <linux/prandom.h>
#else
#include <linux/random.h>
#endif

#include <linux/sched.h>
#include <linux/kthread.h>
#include <linux/workqueue.h>
#include <linux/memblock.h>
#include <linux/ratelimit.h>
#include <linux/notifier.h>
#include <linux/module.h>
#include <linux/fips.h>
#ifndef CONFIG_HUGETLB_PAGE_OPTIMIZE_VMEMMAP
#include <linux/jump_label.h>
#endif
#include <linux/crypto.h>
#include <crypto/algapi.h>
#include <crypto/aead.h>
#include <crypto/hash.h>
#include <crypto/akcipher.h>
#include <crypto/skcipher.h>
#include <crypto/kpp.h>
#include <crypto/aes.h>
#include <crypto/ecdh.h>
#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
#include <crypto/sha.h>
#else
#include <crypto/sha1.h>
#include <crypto/sha2.h>
#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
#include "ecc.h"
#else
#include <crypto/internal/ecc.h>
#endif
#include <crypto/internal/rsa.h>

#if LINUX_VERSION_CODE < KERNEL_VERSION(5,10,0)
#include <crypto/internal/hash.h>
#endif
#include <asm/fpu/api.h>
#include "internal.h"
#include "fips_canister_wrapper_internal.h"
#include <linux/uio.h>
#include <linux/scatterlist.h>
#include <crypto/scatterwalk.h>
#include <crypto/sha1_base.h>
#include <crypto/sha512_base.h>
#include <crypto/sha3.h>

static __ro_after_init bool alg_request_report = false;

/*
 * Replicate a no-op stackleak_track_stack() function for other linux flavours
 * where CONFIG_GCC_PLUGIN_STACKLEAK is disabled to overcome missing symbols.
 * stackleak_track_stack() is inserted for the functions with a stack frame size
 * greater than or equal to CONFIG_STACKLEAK_TRACK_MIN_SIZE.
 */
#ifndef CONFIG_GCC_PLUGIN_STACKLEAK
void __used __no_caller_saved_registers noinstr stackleak_track_stack(void)
{
}
#endif

int fcw_signal_pending(void)
{
	return signal_pending(current);
}

void *fcw_kthread_run(int (*threadfn)(void *data), void *data, const char namefmt[])
{
	struct task_struct *t = kthread_run(threadfn, data, namefmt);
	return (void *)t;
}

int fcw_cond_resched(void)
{
	return cond_resched();
}

void *fcw_kmalloc(size_t size, gfp_t flags)
{
	return kmalloc(size, flags);
}

void *fcw_kzalloc(size_t size, gfp_t flags)
{
	return kzalloc(size, flags);
}

bool fcw_boot_cpu_has(unsigned long bit)
{
	return boot_cpu_has(bit);
}

void * __init fcw_mem_alloc(size_t size)
{
	/* Can be called before mm_init(). */
	if (!slab_is_available())
		return memblock_alloc(size, 8);

	return fcw_kmalloc(size, GFP_KERNEL);
}

void __init fcw_mem_free(void *p)
{
	if (p && slab_is_available() && PageSlab(virt_to_head_page(p)))
		kfree(p);
}

void *fcw_mutex_init(void)
{
	struct mutex *m = kzalloc(sizeof(struct mutex), GFP_KERNEL);
	if (m)
		mutex_init(m);

	return (void *)m;
}

void fcw_mutex_lock(void *m)
{
	mutex_lock((struct mutex *)m);
}

void fcw_mutex_unlock(void *m)
{
	mutex_unlock((struct mutex *)m);
}

bool fcw_schedule_work(struct work_struct *work)
{
	return schedule_work(work);
}

#if LINUX_VERSION_CODE < KERNEL_VERSION(5,10,0)
void kfree_sensitive(const void *p)
{
	kzfree(p);
}

void shash_free_singlespawn_instance(struct shash_instance *inst)
{
	shash_free_instance(shash_crypto_instance(inst));
}

void fips_fail_notify(void)
{
}
#endif

struct aead_request *fcw_aead_request_alloc(struct crypto_aead *tfm,
					    gfp_t gfp)
{
	return aead_request_alloc(tfm, gfp);
}

struct ahash_request *fcw_ahash_request_alloc(struct crypto_ahash *tfm,
					    gfp_t gfp)
{
	return ahash_request_alloc(tfm, gfp);
}

struct akcipher_request *fcw_akcipher_request_alloc(
		struct crypto_akcipher *tfm, gfp_t gfp)
{
	return akcipher_request_alloc(tfm, gfp);
}

struct skcipher_request *fcw_skcipher_request_alloc(
		struct crypto_skcipher *tfm, gfp_t gfp)
{
	return skcipher_request_alloc(tfm, gfp);
}

struct kpp_request *fcw_kpp_request_alloc(
		struct crypto_kpp *tfm, gfp_t gfp)
{
	return kpp_request_alloc(tfm, gfp);
}

u32 fcw_prandom_u32_max(u32 ep_ro)
{
#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
	return prandom_u32_max(ep_ro);
#else
	return get_random_u32_below(ep_ro);
#endif
}

void __noreturn __fcw_module_put_and_kthread_exit(struct module *mod, long code)
{
#if LINUX_VERSION_CODE < KERNEL_VERSION(6,1,0)
	__module_put_and_exit(mod, code);
#else
	__module_put_and_kthread_exit(mod, code);
#endif
}

void fcw_kernel_fpu_begin(void)
{
	kernel_fpu_begin();
}

void fcw_kernel_fpu_end(void)
{
	kernel_fpu_end();
}

void fcw_bug(void)
{
	BUG();
}

void *fcw_init_ratelimit_state(void *rs)
{
	if (rs != NULL)
		return rs;

	struct ratelimit_state *_rs = kzalloc(sizeof(struct ratelimit_state),
					GFP_KERNEL);
	_rs->lock = __RAW_SPIN_LOCK_UNLOCKED(_rs.lock);
	_rs->interval = DEFAULT_RATELIMIT_INTERVAL;
	_rs->burst = DEFAULT_RATELIMIT_BURST;
	_rs->flags = 0;
	return (void *)_rs;
}

bool fcw_ratelimit(void *rs, const char *name)
{
	if (___ratelimit(rs, name))
		return 1;
	return 0;
}

void fcw_bug_on(int cond)
{
	do {
		if (unlikely(cond))
			BUG();
	} while(0);
}

int fcw_warn_on(int cond)
{
	int __ret_warn_on = !!(cond);
	if(unlikely(__ret_warn_on))
		__WARN();
	return unlikely(__ret_warn_on);
}

int fcw_warn_on_once(int cond)
{
	int __ret_warn_on = !!(cond);
	if(unlikely(__ret_warn_on))
		__WARN_FLAGS(BUGFLAG_ONCE | BUGFLAG_TAINT(TAINT_WARN));
	return unlikely(__ret_warn_on);
}

int fcw_warn(int cond, const char *fmt, ...)
{
	int __ret_warn_on = !!(cond);
	if(unlikely(__ret_warn_on))
		__WARN_printf(TAINT_WARN, fmt);
	return unlikely(__ret_warn_on);
}

void *fcw_memcpy(void *dst, const void *src, size_t len)
{
	return memcpy(dst, src, len);
}

size_t fcw_strlcpy(char *dest, const char *src, size_t size)
{
	return strlcpy(dest, src, size);
}

int fcw_sha1_base_do_update(struct shash_desc *desc,
				      const u8 *data,
				      unsigned int len,
				      sha1_block_fn *block_fn)
{
	return sha1_base_do_update(desc, data, len, block_fn);
}

int fcw_sha512_base_do_update(struct shash_desc *desc,
					const u8 *data,
					unsigned int len,
					sha512_block_fn *block_fn)
{
	return sha512_base_do_update(desc, data, len, block_fn);
}
size_t fcw_copy_from_iter(void *addr, size_t bytes, struct iov_iter *i)
{
	return copy_from_iter(addr, bytes, i);
}

void fcw_sg_assign_page(struct scatterlist *sg, struct page *page)
{
	return sg_assign_page(sg, page);
}

void fcw_sg_set_buf(struct scatterlist *sg, const void *buf,
			      unsigned int buflen)
{
	return sg_set_buf(sg, buf, buflen);
}

void *fcw_sg_virt(struct scatterlist *sg)
{
	return sg_virt(sg);
}

void *fcw_scatterwalk_map(struct scatter_walk *walk)
{
	return scatterwalk_map(walk);
}

static char *canister_algs[] = {
	"cipher_null-generic",
	"ecb-cipher_null",
	"rsa-generic",
	"sha1-generic",
	"sha256-generic",
	"sha224-generic",
	"sha512-generic",
	"sha384-generic",
	"aes-generic",
	"ctr(aes-generic)",
	"drbg_pr_ctr_aes128",
	"drbg_pr_ctr_aes192",
	"drbg_pr_ctr_aes256",
	"drbg_pr_sha1",
	"drbg_pr_sha384",
	"drbg_pr_sha512",
	"drbg_pr_sha256",
	"hmac(sha1-generic)",
	"drbg_pr_hmac_sha1",
	"hmac(sha384-generic)",
	"drbg_pr_hmac_sha384",
	"hmac(sha512-generic)",
	"drbg_pr_hmac_sha512",
	"hmac(sha256-generic)",
	"drbg_pr_hmac_sha256",
	"drbg_nopr_ctr_aes128",
	"drbg_nopr_ctr_aes192",
	"drbg_nopr_ctr_aes256",
	"drbg_nopr_sha1",
	"drbg_nopr_sha384",
	"drbg_nopr_sha512",
	"drbg_nopr_sha256",
	"drbg_nopr_hmac_sha1",
	"drbg_nopr_hmac_sha384",
	"drbg_nopr_hmac_sha512",
	"drbg_nopr_hmac_sha256",
	"ecdh-generic",
	"cbc(aes-generic)",
	"ecb(aes-generic)",
	"hmac(sha224-generic)",
	"pkcs1pad(rsa-generic,sha256)",
	"pkcs1pad(rsa-generic,sha512)",
	"xts(ecb(aes-generic))",
	"aes-aesni",
	"__ecb-aes-aesni",
	"__cbc-aes-aesni",
	"__ctr-aes-aesni",
	"__xts-aes-aesni",
	"cryptd(__ecb-aes-aesni)",
	"ecb-aes-aesni",
	"cryptd(__cbc-aes-aesni)",
	"cbc-aes-aesni",
	"cryptd(__ctr-aes-aesni)",
	"ctr-aes-aesni",
	"cryptd(__xts-aes-aesni)",
	"xts-aes-aesni",
	// no certification require
	"crc32c-generic",
	"crct10dif-generic",
};

int fcw_fips_not_allowed_alg(char *name)
{
	if (fips_enabled == 2) {
		int i;
		for (i = 0; i < sizeof(canister_algs)/sizeof(canister_algs[0]); i++) {
			if (strcmp(name, canister_algs[i]) == 0)
				return 0;
		}
		return 1;
	}

	return 0;
}

static int crypto_msg_notify(struct notifier_block *this, unsigned long msg,
			    void *data)
{
	struct crypto_alg *alg = (struct crypto_alg *)data;

	if (msg == CRYPTO_MSG_ALG_REQUEST && alg_request_report) {
		pr_notice("alg request: %s (%s) by %s(%d)",
			   alg->cra_driver_name, alg->cra_name,
			   current->comm, current->pid);
	}

	if (msg == CRYPTO_MSG_ALG_REGISTER) {
		struct crypto_alg *alg = (struct crypto_alg *)data;
		/* Disable non FIPS approved algos */
		if (fcw_fips_not_allowed_alg(alg->cra_driver_name)) {
			pr_err("alg: %s (%s) not certified", alg->cra_driver_name, alg->cra_name);
			crypto_alg_tested(alg->cra_driver_name, -EINVAL);
			return NOTIFY_STOP;

		}
		else if (fips_enabled == 1) {
			pr_notice("alg: %s (%s) is registered in FIPS mode\n", alg->cra_driver_name, alg->cra_name);
		}
	}

	return NOTIFY_DONE;
}

static struct notifier_block crypto_msg_notifier = {
	.notifier_call = crypto_msg_notify,
};

static int __init wrapper_init(void)
{
	return crypto_register_notifier(&crypto_msg_notifier);
}
arch_initcall(wrapper_init);

static int __init alg_request_report_setup(char *__unused)
{
	alg_request_report = true;
	return 1;
}
__setup("alg_request_report", alg_request_report_setup);

static int __init fcw_module_init(void)
{
	fips_integrity_check();
	crypto_self_test_init();
	return true;
}
module_init(fcw_module_init);

static int __init fcw_arch_initcall(void)
{
	cryptomgr_init();
	return true;
}
arch_initcall(fcw_arch_initcall);

static int __init fcw_subsys_initcall(void)
{
	rsa_init();
	crypto_ecb_module_init();
	sha1_generic_mod_init();
	sha256_generic_mod_init();
	sha512_generic_mod_init();
	sha3_generic_mod_init();
	aes_init();
	crypto_ctr_module_init();
	hmac_module_init();
	drbg_init();
	ecdh_init();
	crypto_cbc_module_init();
	xts_module_init();
	crypto_cfb_module_init();
	crypto_ccm_module_init();
	crypto_gcm_module_init();
	ecdsa_init();
	crypto_cts_module_init();
	crypto_cmac_module_init();
	return true;
}
subsys_initcall(fcw_subsys_initcall);

static int __init fcw_late_initcall(void)
{
	aesni_init();
	return true;
}
late_initcall(fcw_late_initcall);

static void __exit fcw_module_exit(void)
{
	cryptomgr_exit();
	crypto_cbc_module_exit();
	crypto_ccm_module_exit();
	crypto_cfb_module_exit();
	crypto_cmac_module_exit();
	crypto_ctr_module_exit();
	crypto_cts_module_exit();
	drbg_exit();
	crypto_ecb_module_exit();
	ecdh_exit();
	ecdsa_exit();
	crypto_gcm_module_exit();
	hmac_module_exit();
	rsa_exit();
	sha1_generic_mod_fini();
	sha256_generic_mod_fini();
	sha512_generic_mod_fini();
	sha3_generic_mod_fini();
	xts_module_exit();
	aesni_exit();
	aes_fini();
}
module_exit(fcw_module_exit);

#ifndef CONFIG_HUGETLB_PAGE_OPTIMIZE_VMEMMAP
DEFINE_STATIC_KEY_FALSE(hugetlb_optimize_vmemmap_key);
EXPORT_SYMBOL(hugetlb_optimize_vmemmap_key);
#endif

/* Export Canister Symbols */
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6,1,0)
EXPORT_SYMBOL(ecc_get_curve25519);
EXPORT_SYMBOL(ecc_get_curve);
EXPORT_SYMBOL(ecc_alloc_point);
EXPORT_SYMBOL(ecc_free_point);
EXPORT_SYMBOL(vli_num_bits);
EXPORT_SYMBOL(ecc_point_is_zero);
#endif
EXPORT_SYMBOL_GPL(crypto_ft_tab);
EXPORT_SYMBOL_GPL(crypto_it_tab);
EXPORT_SYMBOL_GPL(crypto_aes_set_key);
EXPORT_SYMBOL(vli_is_zero);
EXPORT_SYMBOL(vli_from_be64);
EXPORT_SYMBOL(vli_from_le64);
EXPORT_SYMBOL(vli_cmp);
EXPORT_SYMBOL(vli_sub);
EXPORT_SYMBOL(vli_mod_mult_slow);
EXPORT_SYMBOL(vli_mod_inv);
EXPORT_SYMBOL(ecc_point_mult_shamir);
EXPORT_SYMBOL(ecc_is_key_valid);
EXPORT_SYMBOL(ecc_gen_privkey);
EXPORT_SYMBOL(ecc_make_pub_key);
EXPORT_SYMBOL(ecc_is_pubkey_valid_partial);
EXPORT_SYMBOL(ecc_is_pubkey_valid_full);
EXPORT_SYMBOL(crypto_ecdh_shared_secret);
EXPORT_SYMBOL_GPL(crypto_ecdh_key_len);
EXPORT_SYMBOL_GPL(crypto_ecdh_encode_key);
EXPORT_SYMBOL_GPL(crypto_ecdh_decode_key);
EXPORT_SYMBOL_GPL(rsa_parse_pub_key);
EXPORT_SYMBOL_GPL(rsa_parse_priv_key);
EXPORT_SYMBOL_GPL(sha1_zero_message_hash);
EXPORT_SYMBOL(crypto_sha1_update);
EXPORT_SYMBOL(crypto_sha1_finup);
EXPORT_SYMBOL_GPL(sha224_zero_message_hash);
EXPORT_SYMBOL_GPL(sha256_zero_message_hash);
EXPORT_SYMBOL(crypto_sha256_update);
EXPORT_SYMBOL(crypto_sha256_finup);
EXPORT_SYMBOL_GPL(sha384_zero_message_hash);
EXPORT_SYMBOL_GPL(sha512_zero_message_hash);
EXPORT_SYMBOL(crypto_sha512_update);
EXPORT_SYMBOL(crypto_sha512_finup);
EXPORT_SYMBOL_GPL(alg_test);
EXPORT_SYMBOL(crypto_aes_sbox);
EXPORT_SYMBOL(crypto_aes_inv_sbox);
EXPORT_SYMBOL(aes_expandkey);
EXPORT_SYMBOL(aes_encrypt);
EXPORT_SYMBOL(aes_decrypt);
EXPORT_SYMBOL(sha1_transform);
EXPORT_SYMBOL(sha1_init);
EXPORT_SYMBOL(sha256_update);
EXPORT_SYMBOL(sha224_update);
EXPORT_SYMBOL(sha256_final);
EXPORT_SYMBOL(sha224_final);
EXPORT_SYMBOL(sha256);
EXPORT_SYMBOL(crypto_sha3_init);
EXPORT_SYMBOL(crypto_sha3_update);
EXPORT_SYMBOL(crypto_sha3_final);
/* End of Exports */
