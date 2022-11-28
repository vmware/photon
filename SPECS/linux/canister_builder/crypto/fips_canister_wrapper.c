/*
 * Kernel APIs wrapper for the canister.
 *
 * Copyright (C) 2020, 2021, VMware, Inc.
 * Author: Alexey Makhalov <amakhalov@vmware.com>
 *
 */

// Uncomment it in 2023. des3 will not by allowed in FIPS mode.
//#define DES3_IS_NOT_ALLOWED

#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/gfp.h>
#include <linux/slab.h>
#include <linux/mutex.h>
#include <linux/sched.h>
#include <linux/version.h>
#include <linux/workqueue.h>
#ifdef DES3_IS_NOT_ALLOWED
#include <linux/notifier.h>
#include <linux/module.h>
#include <linux/fips.h>
#include <crypto/algapi.h>
#endif
#include <crypto/aead.h>
#include <crypto/hash.h>
#include <crypto/akcipher.h>
#include <crypto/skcipher.h>
#include <crypto/kpp.h>
#if LINUX_VERSION_CODE < KERNEL_VERSION(5,10,0)
#include <crypto/internal/hash.h>
#endif
#include <asm/fpu/api.h>


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

int fcw_fips_not_allowed_alg(char *alg_name)
{
#ifdef DES3_IS_NOT_ALLOWED
	if (strstr(alg_name, "des3_ede"))
		return 1;
#endif
	return 0;
}

#ifdef DES3_IS_NOT_ALLOWED
static int crypto_msg_notify(struct notifier_block *this, unsigned long msg,
			    void *data)
{
	if (msg == CRYPTO_MSG_ALG_REGISTER)
	{
		struct crypto_alg *alg = (struct crypto_alg *)data;
		/* Disable non FIPS approved algos */
		if (fcw_fips_not_allowed_alg(alg->cra_name))
			return NOTIFY_OK;
	}

	return NOTIFY_DONE;
}

static struct notifier_block crypto_msg_notifier = {
	.notifier_call = crypto_msg_notify,
};

static int __init wrapper_init(void)
{
	if (!fips_enabled)
		return 0;

	return crypto_register_notifier(&crypto_msg_notifier);
}
arch_initcall(wrapper_init);
#endif
