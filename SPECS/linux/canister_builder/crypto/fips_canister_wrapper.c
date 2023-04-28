/*
 * Kernel APIs wrapper for the canister.
 *
 * Copyright (C) 2020 - 2022 VMware, Inc.
 * Author: Alexey Makhalov <amakhalov@vmware.com>
 *
 */

#define DES3_IS_NOT_ALLOWED

#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/gfp.h>
#include <linux/slab.h>
#include <linux/mutex.h>
#include <linux/sched.h>
#include <linux/version.h>
#include <linux/workqueue.h>
#include <linux/notifier.h>
#include <linux/module.h>
#include <linux/fips.h>
#include <crypto/algapi.h>
#include <crypto/aead.h>
#include <crypto/hash.h>
#include <crypto/akcipher.h>
#include <crypto/skcipher.h>
#include <crypto/kpp.h>
#if LINUX_VERSION_CODE < KERNEL_VERSION(5,10,0)
#include <crypto/internal/hash.h>
#endif
#include <asm/fpu/api.h>
#include "internal.h"

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


void fcw_kernel_fpu_begin(void)
{
	kernel_fpu_begin();
}

void fcw_kernel_fpu_end(void)
{
	kernel_fpu_end();
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
	"des3_ede-generic",
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
	"jitterentropy_rng",
	"ecdh-generic",
	"cbc(aes-generic)",
	"cbc(des3_ede-generic)",
	"ctr(des3_ede-generic)",
	"ecb(aes-generic)",
	"ecb(des3_ede-generic)",
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
#ifdef DES3_IS_NOT_ALLOWED
	if (strstr(name, "des3_ede"))
		return 1;
#endif
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
		if (fcw_fips_not_allowed_alg(alg->cra_name))
			return NOTIFY_OK;
		if (fcw_fips_not_allowed_alg(alg->cra_driver_name)) {
			pr_err("alg: %s (%s) not certified", alg->cra_driver_name, alg->cra_name);
			crypto_alg_tested(alg->cra_driver_name, -EINVAL);
			return NOTIFY_STOP;

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
