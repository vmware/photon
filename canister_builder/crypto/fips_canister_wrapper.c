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
#include <linux/spinlock.h>
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
#include <linux/uio.h>
#include <linux/scatterlist.h>
#include <crypto/scatterwalk.h>
#include <crypto/sha1_base.h>
#include <crypto/sha512_base.h>
#include <crypto/sha3.h>
#include <crypto/internal/geniv.h>
#include "fips_canister_wrapper_common.h"

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

extern void fcw_sg_set_buf(struct scatterlist *sg, const void *buf, unsigned int buflen);
extern int fcw_warn_on(int cond);
extern size_t fcw_copy_from_iter(void *addr, size_t bytes, struct iov_iter *i);
extern void *fcw_memcpy(void *dst, const void *src, size_t len);

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

void *fcw_spin_lock_init(void)
{
	spinlock_t *lock = kzalloc(sizeof(struct spinlock), GFP_KERNEL);
	if (lock)
		spin_lock_init(lock);
	return (void *)lock;
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

int fcw_is_warn_true(int cond)
{
	int __ret_warn_on = !!(cond);
	return unlikely(__ret_warn_on);
}
void fcw_warn(void)
{
	__WARN_FLAGS(BUGFLAG_NO_CUT_HERE | BUGFLAG_TAINT(TAINT_WARN));
}

void *fcw_memcpy(void *dst, const void *src, size_t len)
{
	return memcpy(dst, src, len);
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

void *fcw_sg_page_address(struct scatterlist *sg)
{
	struct page *page = sg_page(sg);
	return page_address(page);
}

static unsigned int count_test_sg_divisions(const struct test_sg_division *divs)
{
	unsigned int remaining = TEST_SG_TOTAL;
	unsigned int ndivs = 0;

	do {
		remaining -= divs[ndivs++].proportion_of_total;
	} while (remaining);

	return ndivs;
}

static void testmgr_poison(void *addr, size_t len)
{
	memset(addr, TESTMGR_POISON_BYTE, len);
}

/**
 * build_test_sglist() - build a scatterlist for a crypto test
 *
 * @tsgl: the scatterlist to build.  @tsgl->bufs[] contains an array of 2-page
 *       buffers which the scatterlist @tsgl->sgl[] will be made to point into.
 * @divs: the layout specification on which the scatterlist will be based
 * @alignmask: the algorithm's alignmask
 * @total_len: the total length of the scatterlist to build in bytes
 * @data: if non-NULL, the buffers will be filled with this data until it ends.
 *       Otherwise the buffers will be poisoned.  In both cases, some bytes
 *       past the end of each buffer will be poisoned to help detect overruns.
 * @out_divs: if non-NULL, the test_sg_division to which each scatterlist entry
 *           corresponds will be returned here.  This will match @divs except
 *           that divisions resolving to a length of 0 are omitted as they are
 *           not included in the scatterlist.
 *
 * Return: 0 or a -errno value
 */
static int build_test_sglist(struct test_sglist *tsgl,
			     const struct test_sg_division *divs,
			     const unsigned int alignmask,
			     const unsigned int total_len,
			     struct iov_iter *data,
			     const struct test_sg_division *out_divs[XBUFSIZE])
{
	struct {
		const struct test_sg_division *div;
		size_t length;
	} partitions[XBUFSIZE];
	const unsigned int ndivs = count_test_sg_divisions(divs);
	unsigned int len_remaining = total_len;
	unsigned int i;

	BUILD_BUG_ON(ARRAY_SIZE(partitions) != ARRAY_SIZE(tsgl->sgl));
	if (fcw_warn_on(ndivs > ARRAY_SIZE(partitions)))
		return -EINVAL;

	/* Calculate the (div, length) pairs */
	tsgl->nents = 0;
	for (i = 0; i < ndivs; i++) {
		unsigned int len_this_sg =
			     min(len_remaining,
			     (total_len * divs[i].proportion_of_total +
			     TEST_SG_TOTAL / 2) / TEST_SG_TOTAL);

		if (len_this_sg != 0) {
			partitions[tsgl->nents].div = &divs[i];
			partitions[tsgl->nents].length = len_this_sg;
			tsgl->nents++;
			len_remaining -= len_this_sg;
		}
	}
	if (tsgl->nents == 0) {
		partitions[tsgl->nents].div = &divs[0];
		partitions[tsgl->nents].length = 0;
		tsgl->nents++;
	}
	partitions[tsgl->nents - 1].length += len_remaining;

	/* Set up the sgl entries and fill the data or poison */
	sg_init_table(tsgl->sgl, tsgl->nents);
	for (i = 0; i < tsgl->nents; i++) {
		unsigned int offset = partitions[i].div->offset;
		void *addr;
		if (partitions[i].div->offset_relative_to_alignmask)
			offset += alignmask;
		while (offset + partitions[i].length + TESTMGR_POISON_LEN > 2 * PAGE_SIZE) {
			if (fcw_warn_on(offset <= 0))
				return -EINVAL;
			offset /= 2;
		}

		addr = &tsgl->bufs[i][offset];
		fcw_sg_set_buf(&tsgl->sgl[i], addr, partitions[i].length);
		if (out_divs)
			out_divs[i] = partitions[i].div;

		if (data) {
			size_t copy_len, copied;

			copy_len = min(partitions[i].length, data->count);
			copied = fcw_copy_from_iter(addr, copy_len, data);
			if (fcw_warn_on(copied != copy_len))
				return -EINVAL;
			testmgr_poison(addr + copy_len, partitions[i].length +
				       TESTMGR_POISON_LEN - copy_len);
		} else {
			testmgr_poison(addr, partitions[i].length +
				       TESTMGR_POISON_LEN);
		}
	}

	sg_mark_end(&tsgl->sgl[tsgl->nents - 1]);
	tsgl->sgl_ptr = tsgl->sgl;
	fcw_memcpy(tsgl->sgl_saved, tsgl->sgl, tsgl->nents * sizeof(tsgl->sgl[0]));
	return 0;
}

int fcw_build_hash_sglist(struct test_sglist *tsgl,
			     const struct hash_testvec *vec,
			     const struct testvec_config *cfg,
			     unsigned int alignmask,
			     const struct test_sg_division *divs[XBUFSIZE])
{
	struct kvec kv;
	struct iov_iter input;

	kv.iov_base = (void *)vec->plaintext;
	kv.iov_len = vec->psize;
	iov_iter_kvec(&input, WRITE, &kv, 1, vec->psize);
	return build_test_sglist(tsgl, cfg->src_divs, alignmask, vec->psize,
				 &input, divs);
}

/* Build the src and dst scatterlists for an skcipher or AEAD test */
int fcw_build_cipher_test_sglists(struct cipher_test_sglists *tsgls,
				  const struct testvec_config *cfg,
				  unsigned int alignmask,
				  unsigned int src_total_len,
				  unsigned int dst_total_len,
				  const struct kvec *inputs,
				  unsigned int nr_inputs)
{
	struct iov_iter input;
	int err;

	iov_iter_kvec(&input, WRITE, inputs, nr_inputs, src_total_len);
	err = build_test_sglist(&tsgls->src, cfg->src_divs, alignmask,
				cfg->inplace_mode != OUT_OF_PLACE ?
					max(dst_total_len, src_total_len) :
					src_total_len,
				&input, NULL);
	if (err)
		return err;

	/*
	 * In-place crypto operations can use the same scatterlist for both the
	 * source and destination (req->src == req->dst), or can use separate
	 * scatterlists (req->src != req->dst) which point to the same
	 * underlying memory.  Make sure to test both cases.
	 */
	if (cfg->inplace_mode == INPLACE_ONE_SGLIST) {
		tsgls->dst.sgl_ptr = tsgls->src.sgl;
		tsgls->dst.nents = tsgls->src.nents;
		return 0;
	}
	if (cfg->inplace_mode == INPLACE_TWO_SGLISTS) {
		/*
		 * For now we keep it simple and only test the case where the
		 * two scatterlists have identical entries, rather than
		 * different entries that split up the same memory differently.
		 */
		fcw_memcpy(tsgls->dst.sgl, tsgls->src.sgl,
		       tsgls->src.nents * sizeof(tsgls->src.sgl[0]));
		fcw_memcpy(tsgls->dst.sgl_saved, tsgls->src.sgl,
		       tsgls->src.nents * sizeof(tsgls->src.sgl[0]));
		tsgls->dst.sgl_ptr = tsgls->dst.sgl;
		tsgls->dst.nents = tsgls->src.nents;
		return 0;
	}
	/* Out of place */
	return build_test_sglist(&tsgls->dst,
				 cfg->dst_divs[0].proportion_of_total ?
					cfg->dst_divs : cfg->src_divs,
				 alignmask, dst_total_len, NULL, NULL);
}

struct scatterlist *fcw_scatterwalk_ffwd(struct scatterlist dst[2],
				     struct scatterlist *src,
				     unsigned int len)
{
	return scatterwalk_ffwd(dst, src, len);
}

void fcw_scatterwalk_unmap(void *vaddr)
{
	return scatterwalk_unmap(vaddr);
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
	"cbc(aes-aesni)",
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
	"ccm_base(ctr(aes-generic),cbcmac(aes-generic))",
	"ccm_base(ctr-aes-aesni,cbcmac(aes-aesni))",
	"cfb(aes-generic)",
	"cfb(aes-aesni)",
	"cmac(aes-generic)",
	"cmac(aes-aesni)",
	"sha3-224-generic",
	"hmac(sha3-224-generic)",
	"sha3-256-generic",
	"hmac(sha3-256-generic)",
	"sha3-384-generic",
	"hmac(sha3-384-generic)",
	"sha3-512-generic",
	"hmac(sha3-512-generic)",
	"pkcs1pad(rsa-generic,sha1)",
	"pkcs1pad(rsa-generic,sha224)",
	"pkcs1pad(rsa-generic,sha384)",
	"ecdsa-nist-p384-generic",
	"ecdsa-nist-p256-generic",
	"ecdh-nist-p384-generic",
	"ecdh-nist-p256-generic",
	"jitterentropy_rng",
	"cts-cbc-aes-aesni",
	"__cts-cbc-aes-aesni",
	"cryptd(__cts-cbc-aes-aesni)",
	"seqiv(rfc4106-gcm-aesni)",
	"seqiv(rfc4106(gcm_base(ctr(aes-generic),ghash-generic)))",
	"ghash-generic",
	"cts(cbc(aes-generic))",
	"cts(cbc(aes-generic))",
	"cryptd(__cbc-aes-aesni)",
	"cbc-aes-aesni",
	"gcm_base(ctr(aes-generic),ghash-generic)",
	"generic-gcm-aesni",
	"__generic-gcm-aesni",
	"cryptd(__generic-gcm-aesni)",
	"rfc4106(gcm_base(ctr(aes-generic),ghash-generic))",
	"rfc4106-gcm-aesni",
	"__rfc4106-gcm-aesni",
	"cryptd(__rfc4106-gcm-aesni)",
	// no certification require
	"crc32c-generic",
	"crct10dif-generic",
	"crc32c-intel",
	"crc64-rocksoft-generic",
	"deflate-scomp",
	"deflate-generic",
	"zlib-deflate-scomp",
	"__xctr-aes-aesni",
	"xctr-aes-aesni",
};

int fcw_fips_not_allowed_alg(char *name)
{
	if (fips_enabled == 1) {
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
		if (fcw_fips_not_allowed_alg(alg->cra_driver_name)) {
			pr_notice("alg: %s (%s) not certified", alg->cra_driver_name, alg->cra_name);
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
EXPORT_SYMBOL_GPL(aead_geniv_alloc);
EXPORT_SYMBOL_GPL(aead_init_geniv);
EXPORT_SYMBOL_GPL(aead_exit_geniv);
/* End of Exports */
