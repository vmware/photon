/*
 * Test module for externalizing the crypto API to use for CAVS testing
 *
 * Copyright (c) 2015 - 2022 Stephan Mueller <smueller@chronox.de>
 *
 * License: see LICENSE file
 *
 * THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ALL OF
 * WHICH ARE HEREBY DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
 * OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF NOT ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 */

/*
 * The interface description is given with struct kccavs_debugfs below
 */
#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt

#include <linux/version.h>
#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/stat.h>
#include <linux/scatterlist.h>
#include <linux/crypto.h>

#include <crypto/rng.h>
#include <crypto/hash.h>
#include <crypto/drbg.h>
#include <crypto/skcipher.h>

#include <linux/debugfs.h>

/************** END Configuration ************/

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stephan Mueller <smueller@chronox.de>");
MODULE_DESCRIPTION("Externalization of crypto API to user space");

#define MAXNAME 64	/* consistent with the AF_ALG interface size */
#define MAXLEN		(16 * PAGE_SIZE)	/* IV and Key should fit */
#define MAXDATALEN	65537 /* data to be processed */

/* cipher types of the kernel crypto API */
#define ABLKCIPHER	0x00000001
#define SHASH		0x00000002
#define DRBG		0x00000008
#define BLKCIPHER	0x00000100

#define TYPE_KEEP	0x01000000 /* keep cipher mode open, needed
				      for Monte Carlo cipher tests
				      which need the chaining mode state*/
#define TYPE_ENC	0x02000000 /* Encryption operation */
#define TYPE_DEC	0x04000000 /* Decryption operation */

/* debug macro */
#if 0
#define dbg(fmt, ...) pr_info(fmt, ##__VA_ARGS__)
#else
#define dbg(fmt, ...)
#endif

/*
 * kzfree was renamed to kfree_sensitive in 5.9
 */
#undef free_zero
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5,9,0)
# define free_zero(x)	kfree_sensitive(x)
#else
# define free_zero(x)	kzfree(x)
#endif

struct kccavs_data {
	char *data;
	u64 len;
	u64 maxlen;
};

/************* Async testing ***********/
struct kccavs_tcrypt_res {
	struct completion completion;
	int err;
};

/* tie all data structures together */
struct kccavs_async_def {
	struct crypto_skcipher *tfm;
	struct skcipher_request *req;
	struct kccavs_tcrypt_res result;
};

struct kccavs_test {
	char name[MAXNAME];	/* cra_name or cra_driver_name */
	u32 type; /* hold the ORed cipher types listed above */
	u32 keylen;
	struct kccavs_data key; /* key for a crypto operation */
	struct kccavs_data data; /* data for the crypto operation */
	struct kccavs_data iv; /* iv for the crypto operation */
	struct kccavs_data entropy; /* DRBG entropy */
	struct kccavs_data entpra; /* DRBG 1st reseed entropy */
	struct kccavs_data entprb; /* DRBG 2nd reseed entropy */
	struct kccavs_data addtla; /* DRBG 1st addtl data string */
	struct kccavs_data addtlb; /* DRBG 1st addtl data string */
	struct kccavs_data entropyreseed; /* DRBG reseed entropy */
	struct kccavs_data addtlreseed; /* DRBG reseed addtl data string */
	struct kccavs_data pers; /* DRBG personalization string */

	struct kccavs_async_def *ablk; /* ablkcipher handle */
        struct crypto_blkcipher *blkcipher; /* block cipher handle */
};


/* this data structure holds the state of the cipher operation.
 * As we use one global variable, the entire kernel module must be used
 * single threaded!
 *
 * To change it to multi-threaded:
 *	- one init file -> creates sub dir with interface files
 *	- register one kccavs_test instance in directory filp->private_data
 *      - convert all calls below to fetch the right private_data
 */
struct kccavs_test *kccavs_test;

/*
 * This data structure holds the dentry's of the debugfs files establishing
 * the interface to user space. Reading or writing into these files set the
 * cryptoapi-test machinery in motion.
 *
 * The following files are defined within the directory of
 * /sys/kernel/debug/kcapi_lrng:
 *
 * type: Cipher type using the u64 integer defines listed above
 * key: If a cipher needs a key (HMAC, sym. ciphers, RNG seed), it must be
 *	written into this file (i.e. echo -n "abc" > key). Note, the kernel
 *	expects a binary value.
 * iv: Just like key, but holding the IV. This variable is pulled, if needed.
 * data: This file is the main input/output file. Any data to be hashed/encrypted/
 *	 decrypted by the chosen cipher must be written into this file. When
 *	 reading this file, the cipher operation happens and the contents in this
 *	 file holds the result of the cipher operation. Note, every read system
 *	 call invokes a new round of ciphers where the contents of data is used
 *	 as input to the cipher! You usually cannot use the cat command as it
 *	 uses two read system calls to complete one read. The file treats all
 *	 data as binary.
 * datalen: This is a superflowous, but possibly interesting file as it holds
 *	    the data length of the string found in data.
 */
struct kccavs_debugfs {
	struct dentry *kccavs_debugfs_root; /* /sys/kernel/debug/kcapi_lrng */
	struct dentry *kccavs_debugfs_name; /* .../name */
	struct dentry *kccavs_debugfs_type; /* .../type */
	struct dentry *kccavs_debugfs_keylen; /* .../keylen */
	struct dentry *kccavs_debugfs_key; /* .../key */
	struct dentry *kccavs_debugfs_data; /* .../data */
	struct dentry *kccavs_debugfs_iv; /* .../iv */

	struct dentry *kccavs_debugfs_drbg_entropy; /* .../drbg_entropy */
	struct dentry *kccavs_debugfs_drbg_entpra; /* .../drbg_entpra */
	struct dentry *kccavs_debugfs_drbg_entprb; /* .../drbg_entprb */
	struct dentry *kccavs_debugfs_drbg_addtla; /* .../drbg_addtla */
	struct dentry *kccavs_debugfs_drbg_addtlb; /* .../drbg_addtlb */
	struct dentry *kccavs_debugfs_drbg_entropyreseed; /* .../drbg_entropyreseed */
	struct dentry *kccavs_debugfs_drbg_addtlreseed; /* .../drbg_addtlreseed */
	struct dentry *kccavs_debugfs_drbg_pers; /* .../drbg_pers */
};

struct kccavs_debugfs *kccavs_debugfs;

struct kccavs_test_desc {
	const u64 alg;
	int (*test)(size_t nbytes);
};

struct sdesc {
	struct shash_desc shash;
	char ctx[];
};

static struct sdesc *kccavs_init_sdesc(struct crypto_shash *alg)
{
	struct sdesc *sdesc;
	int size;

	size = sizeof(struct shash_desc) + crypto_shash_descsize(alg);
	sdesc = kmalloc(size, GFP_KERNEL);
	if (!sdesc)
		return ERR_PTR(-ENOMEM);
	sdesc->shash.tfm = alg;
#if LINUX_VERSION_CODE < KERNEL_VERSION(5,1,0)
	sdesc->shash.flags = 0x0;
#endif
	return sdesc;
}

static void kccavs_free_cipher(void)
{
	if (kccavs_test->ablk != NULL) {
		crypto_free_skcipher(kccavs_test->ablk->tfm);
		skcipher_request_free(kccavs_test->ablk->req);
		kfree(kccavs_test->ablk);
		kccavs_test->ablk = NULL;
	}
}

static void kccavs_scrub(void)
{
	memset(kccavs_test->name, 0, MAXNAME);
	memset(kccavs_test->key.data, 0, MAXDATALEN);
	kccavs_test->key.len = 0;
	memset(kccavs_test->data.data, 0, MAXDATALEN);
	kccavs_test->data.len = 0;
	memset(kccavs_test->iv.data, 0, MAXLEN);
	kccavs_test->iv.len = 0;
	memset(kccavs_test->entropy.data, 0, MAXLEN);
	kccavs_test->entropy.len = 0;
	memset(kccavs_test->entpra.data, 0, MAXLEN);
	kccavs_test->entpra.len = 0;
	memset(kccavs_test->entprb.data, 0, MAXLEN);
	kccavs_test->entprb.len = 0;
	memset(kccavs_test->addtla.data, 0, MAXLEN);
	kccavs_test->addtla.len = 0;
	memset(kccavs_test->addtlb.data, 0, MAXLEN);
	kccavs_test->addtlb.len = 0;
	memset(kccavs_test->entropyreseed.data, 0, MAXLEN);
	kccavs_test->entropyreseed.len = 0;
	memset(kccavs_test->addtlreseed.data, 0, MAXLEN);
	kccavs_test->addtlreseed.len = 0;
	memset(kccavs_test->pers.data, 0, MAXLEN);
	kccavs_test->pers.len = 0;
	kccavs_test->type = 0;
	kccavs_test->keylen = 0;

	kccavs_free_cipher();
}

/*
 * input: type
 * input: name
 * input: plaintext / ciphertext in kccavs_test->data
 * input: key in kccavs_test->key
 * input: IV in kccavs_test->iv
 * output: ciphertext / plaintext in kccavs_test->data
 */
static int kccavs_test_blkcipher(size_t nbytes)
{
	struct scatterlist sg;
	int ret = -EFAULT;
	struct kccavs_data *data = &kccavs_test->data;
	struct kccavs_data *key = &kccavs_test->key;
	struct kccavs_data *iv = &kccavs_test->iv;
	
	/*
	 * we explicitly do not check the input buffer as
	 * we allow an empty string.
	 */
	if (kccavs_test->ablk == NULL) {
		struct crypto_skcipher *tfm = NULL;
		struct skcipher_request *req = NULL;

		kccavs_test->ablk = kzalloc(sizeof(struct kccavs_async_def),
					    GFP_KERNEL);
		if (!kccavs_test->ablk) {
			pr_info("could not allocate ablkcipher global handle for %s\n", kccavs_test->name);
			return -ENOMEM;
		}

		tfm = crypto_alloc_skcipher(kccavs_test->name, 0,
					    CRYPTO_ALG_ASYNC);
		if (IS_ERR(tfm)) {
			pr_info("could not allocate ablkcipher handle for %s %ld\n",
			kccavs_test->name, PTR_ERR(tfm));
			ret = PTR_ERR(tfm);
			goto out;
		}

		req = skcipher_request_alloc(tfm, GFP_KERNEL);
		if (!req) {
			pr_info("could not allocate request queue\n");
			ret = -ENOMEM;
			goto out;
		}
		kccavs_test->ablk->tfm = tfm;
		kccavs_test->ablk->req = req;

		ret = crypto_skcipher_setkey(tfm, key->data, key->len);
		if (ret) {
			pr_info("key could not be set %d\n", ret);
			ret = -EINVAL;
			goto out;
		}

		skcipher_request_set_callback(req, 0, NULL, NULL);
	}

	sg_init_one(&sg, data->data, data->len);
	skcipher_request_set_crypt(kccavs_test->ablk->req, &sg, &sg,
				   data->len, iv->data);

	if (kccavs_test->type & TYPE_ENC)
		ret = crypto_skcipher_encrypt(kccavs_test->ablk->req);
	else
		ret = crypto_skcipher_decrypt(kccavs_test->ablk->req);

out:
	if (!(kccavs_test->type & TYPE_KEEP)) {
		kccavs_free_cipher();
	}
	return ret;
}

/* Callback function */
static void kccavs_ablkcipher_cb(struct crypto_async_request *req, int error)
{
	struct kccavs_tcrypt_res *result = req->data;

	if (error == -EINPROGRESS)
		return;
	result->err = error;
	complete(&result->completion);
	dbg("ablkcipher operation finished successfully\n");
}

/* Perform encryption or decryption */
static unsigned int kccavs_ablkcipher_encdec(struct kccavs_async_def *def,
					     int enc)
{
	int rc = 0;

	init_completion(&def->result.completion);

	if (enc)
		rc = crypto_skcipher_encrypt(def->req);
	else
		rc = crypto_skcipher_decrypt(def->req);

	switch (rc) {
	case 0:
		break;
	case -EINPROGRESS:
	case -EBUSY:
		wait_for_completion(&def->result.completion);
		if (!def->result.err) {
			reinit_completion(&def->result.completion);
		}
		break;
	default:
		dbg("Async cipher operation returned with %d"
		    " result %d\n",rc, def->result.err);
		break;
	}

	return rc;
}

/*
 * ABLKCIPHER encryption and decryption
 * input: type
 * input: name
 * input: plaintext / ciphertext in kccavs_test->data
 * input: IV in kccavs_test->iv
 * input: key in kccavs_test->key
 * output: ciphertext / plaintext in kccavs_test->data
 *
 * Note: for decryption, the data->data will contain deadbeef if the
 *	 authentication failed (KW).
 */
static int kccavs_test_ablkcipher(size_t nbytes)
{
	int ret = -EFAULT;
	struct scatterlist sg;
	struct kccavs_data *data = &kccavs_test->data;
	struct kccavs_data *iv = &kccavs_test->iv;
	struct kccavs_data *key = &kccavs_test->key;

	if (kccavs_test->ablk == NULL) {
		struct crypto_skcipher *tfm = NULL;
		struct skcipher_request *req = NULL;

		kccavs_test->ablk = kzalloc(sizeof(struct kccavs_async_def),
					    GFP_KERNEL);
		if (!kccavs_test->ablk) {
			pr_info("could not allocate ablkcipher global handle for %s\n", kccavs_test->name);
			return -ENOMEM;
		}

		tfm = crypto_alloc_skcipher(kccavs_test->name, 0, 0);
		if (IS_ERR(tfm)) {
			pr_info("could not allocate ablkcipher handle for %s %ld\n",
			kccavs_test->name, PTR_ERR(tfm));
			ret = PTR_ERR(tfm);
			goto out;
		}

		req = skcipher_request_alloc(tfm, GFP_KERNEL);
		if (!req) {
			pr_info("could not allocate request queue\n");
			ret = -ENOMEM;
			goto out;
		}
		kccavs_test->ablk->tfm = tfm;
		kccavs_test->ablk->req = req;

		ret = crypto_skcipher_setkey(tfm, key->data, key->len);
		if (ret) {
			pr_info("key could not be set %d\n", ret);
			ret = -EINVAL;
			goto out;
		}

		skcipher_request_set_callback(req, CRYPTO_TFM_REQ_MAY_BACKLOG,
					kccavs_ablkcipher_cb,
					&kccavs_test->ablk->result);

		if (kccavs_test->type & TYPE_ENC && data->len > MAXDATALEN)
		{
			pr_info("input data too long for %s\n", kccavs_test->name);
			ret = -ENOSPC;
			goto out;
		}

	}

	sg_init_one(&sg, data->data, data->len);
	skcipher_request_set_crypt(kccavs_test->ablk->req, &sg, &sg,
				   data->len, iv->data);

	if (kccavs_test->type & TYPE_ENC) {
		ret = kccavs_ablkcipher_encdec(kccavs_test->ablk, 1);
		if (0 > ret) {
			pr_info("ablkcipher encryption failed: %d\n", ret);
		}
	} else {
		ret = kccavs_ablkcipher_encdec(kccavs_test->ablk, 0);
		/* only defined for KW */
		if (-EBADMSG == ret ||
		    -EBADMSG == kccavs_test->ablk->result.err) {
			memset(data->data, 0, data->len);
			memcpy(data->data, "\xde\xad\xbe\xef", 4);
			data->len = 4;
			ret = 0;
		} else if (0 > ret) {
			pr_info("ablkcipher decryption failed %d\n", ret);
		}
	}

out:
	if (!(kccavs_test->type & TYPE_KEEP))
		kccavs_free_cipher();
	return ret;
}

/*
 * input: type
 * input: name
 * input: message in kccavs_test->data
 * input: key in kccavs_test->key if TYPE_HMAC
 * output: digest in kccavs_test->data
 */
static int kccavs_test_hash(size_t nbytes)
{
	int ret;
	struct crypto_shash *tfm;
	struct kccavs_data *data = &kccavs_test->data;
	struct kccavs_data *key = &kccavs_test->key;
	unsigned char *digest = NULL;
	struct sdesc *sdesc = NULL;

	/*
	 * We explicitly do not check the input buffer as we allow
	 * an empty string.
	 */

	/* allocate synchronous hash */
	tfm = crypto_alloc_shash(kccavs_test->name, 0, 0);
	if (IS_ERR(tfm)) {
		pr_info("could not allocate digest TFM handle for %s\n", kccavs_test->name);
		return PTR_ERR(tfm);
	}

	ret = -ENOMEM;
	digest = kzalloc(crypto_shash_digestsize(tfm), GFP_KERNEL);
	if (!digest)
		goto out;

	/* make room for scratch memory */
	sdesc = kccavs_init_sdesc(tfm);
	if (!sdesc) {
		goto out;
	}

	if (key->len) {
		dbg("set key for HMAC\n");
		ret = crypto_shash_setkey(tfm, key->data, key->len);
		if (ret < 0)
			goto out;
	}

	ret = crypto_shash_digest(&sdesc->shash, data->data, data->len, digest);
	if (!ret) {
		data->len = crypto_shash_digestsize(tfm);
		memcpy(data->data, digest, data->len);
	}

out:
	free_zero(sdesc);
	free_zero(digest);
	crypto_free_shash(tfm);
	return ret;
}

/*
 * DRBG testing
 *
 * input: entropy data
 * input: size of random number to be generated supplied by the bytes value in
 * 	  the read() system call of data
 * input: 1st PR entropy (if applicable)
 * input: 2nd PR entropy (if applicable)
 * input: 1st additional input string (if applicable)
 * input: 2nd additional input string (if applicable)
 * input: personalization string (if applicable)
 * output: random number in data
 * return:
 * 	>0 when random number was generated
 * 	error code otherwise
 */
static int kccavs_test_drbg(size_t nbytes)
{
	int ret = -EAGAIN;
	struct crypto_rng *drng;
	struct kccavs_data *data = &kccavs_test->data;
	struct kccavs_data *entropy = &kccavs_test->entropy;
	struct kccavs_data *entpra = &kccavs_test->entpra;
	struct kccavs_data *entprb = &kccavs_test->entprb;
	struct kccavs_data *addtla = &kccavs_test->addtla;
	struct kccavs_data *addtlb = &kccavs_test->addtlb;
	struct kccavs_data *entropyreseed = &kccavs_test->entropyreseed;
	struct kccavs_data *addtlreseed = &kccavs_test->addtlreseed;
	struct kccavs_data *persinput = &kccavs_test->pers;
	struct drbg_test_data test_data;
	struct drbg_string addtl, pers, testentropy;

	data->len = nbytes;
	memset(data->data, 0, MAXDATALEN);

	drng = crypto_alloc_rng(kccavs_test->name, 0, 0);
	if(IS_ERR(drng))
	{
		pr_info("could not allocate DRNG handle for %s\n",
			kccavs_test->name);
		return PTR_ERR(drng);
	}
	dbg("testing DRNG %s\n", kccavs_test->name);

	test_data.testentropy = &testentropy;
	if (!entropy->data || !entropy->len) {
		ret = crypto_rng_get_bytes(drng, data->data, nbytes);
		goto out;
	}
	drbg_string_fill(&testentropy, entropy->data, entropy->len);
	drbg_string_fill(&pers, persinput->data, persinput->len);
	ret = crypto_drbg_reset_test(drng, &pers, &test_data);
	if (ret) {
		pr_info("Failed to reset rng\n");
		goto out;
	}
	dbg("testing DRNG %s reset\n", kccavs_test->name);

	if (entropyreseed->len) {
		drbg_string_fill(&testentropy, entropyreseed->data,
				 entropyreseed->len);
		drbg_string_fill(&addtl, addtlreseed->data, addtlreseed->len);
		ret = crypto_drbg_reset_test(drng, &addtl, &test_data);
		if (ret < 0) {
			pr_info("could not seed DRBG\n");
			goto out;
		}
	}

	drbg_string_fill(&addtl, addtla->data, addtla->len);
	if (entpra->len) {
		drbg_string_fill(&testentropy, entpra->data, entpra->len);
		ret = crypto_drbg_get_bytes_addtl_test(drng,
			data->data, nbytes, &addtl, &test_data);
	} else {
		ret = crypto_drbg_get_bytes_addtl(drng,
			data->data, nbytes, &addtl);
	}
	if (ret < 0) {
		pr_info("could not obtain random data\n");
		goto out;
	}

	drbg_string_fill(&addtl, addtlb->data, addtlb->len);
	if (entprb->len) {
		drbg_string_fill(&testentropy, entprb->data, entprb->len);
		ret = crypto_drbg_get_bytes_addtl_test(drng,
			data->data, nbytes, &addtl, &test_data);
	} else {
		ret = crypto_drbg_get_bytes_addtl(drng,
			data->data, nbytes, &addtl);
	}

	if (ret < 0)
		pr_info("could not obtain random data\n");

	ret = 0;

out:
	crypto_free_rng(drng);
	return ret;
}

/****************************************************************************
 ****************** Perform testing *****************************************
 ****************************************************************************/

/*
 * Initiate the actual crypto work and invoke the call back functions handling
 * the requested cipher operation.
 */
static int kccavs_do_calc(size_t nbytes)
{
	int ret = -EINVAL;

	if (!kccavs_test->type) {
		printk("no type provided\n");
		return ret;
	}

	if (!kccavs_test->name) {
		printk("no name provided\n");
		return ret;
	}

	dbg("Test will be executed with name %s and type %lx\n",
	    kccavs_test->name, (unsigned long int) kccavs_test->type);

	if ((kccavs_test->type & SHASH) == SHASH) {
		ret = kccavs_test_hash(nbytes);
	} else if ((kccavs_test->type & ABLKCIPHER) == ABLKCIPHER) {
		ret = kccavs_test_ablkcipher(nbytes);
	} else if ((kccavs_test->type & DRBG) == DRBG) {
		ret = kccavs_test_drbg(nbytes);
	} else if ((kccavs_test->type & BLKCIPHER) == BLKCIPHER) {
		ret = kccavs_test_blkcipher(nbytes);
	} else {
		pr_info("Unknown cipher parameter\n");
		return -EINVAL;
	}

	return ret;
}

/* DebugFS operations and definition of the debugfs files */

static ssize_t kccavs_write_common(struct file *file, const char __user *buf,
			           size_t nbytes, loff_t *ppos,
				   struct kccavs_data *data)
{
	if (nbytes > data->maxlen - 1)
		return -E2BIG;
	data->len = nbytes;
	memset(data->data, 0, data->maxlen);

	/* we got a zero data */
	if (nbytes == 0)
		return nbytes;

	return simple_write_to_buffer(data->data, data->len, ppos, buf, nbytes);
}

static ssize_t kccavs_name_read(struct file *file, char __user *buf,
			      size_t nbytes, loff_t *ppos)
{
	char *name = kccavs_test->name;
	return simple_read_from_buffer(buf, nbytes, ppos, name, MAXNAME);
}

static ssize_t kccavs_name_write(struct file *file, const char __user *buf,
			       size_t nbytes, loff_t *ppos)
{
	char *name = kccavs_test->name;

	if (nbytes > MAXNAME-1)
		return -E2BIG;
	/* clear full data structure */
	kccavs_scrub();
	if (nbytes == 0)
		return nbytes;
	return simple_write_to_buffer(name, MAXNAME-1, ppos, buf, nbytes);
}

static ssize_t kccavs_key_read(struct file *file, char __user *buf,
				  size_t nbytes, loff_t *ppos)
{
	struct kccavs_data *key = &kccavs_test->key;
	return simple_read_from_buffer(buf, nbytes, ppos, key->data, key->len);
}

static ssize_t kccavs_key_write(struct file *file, const char __user *buf,
				size_t nbytes, loff_t *ppos)
{
	/*
	 * As the key is modified / set, deallocate all handles as they need to
	 * be reinitialized.
	 */
	kccavs_free_cipher();

	return kccavs_write_common(file, buf, nbytes, ppos, &kccavs_test->key);
}

static ssize_t kccavs_iv_read(struct file *file, char __user *buf,
			      size_t nbytes, loff_t *ppos)
{
	struct kccavs_data *iv = &kccavs_test->iv;

	return simple_read_from_buffer(buf, nbytes, ppos, iv->data, iv->len);
}

static ssize_t kccavs_iv_write(struct file *file, const char __user *buf,
			       size_t nbytes, loff_t *ppos)
{
	/*
	 * as the IV is modified / set, deallocate all handles as they need to
	 * be reinitialized.
	 */
	kccavs_free_cipher();

	return kccavs_write_common(file, buf, nbytes, ppos, &kccavs_test->iv);
}

static ssize_t kccavs_data_read(struct file *file, char __user *buf,
				size_t nbytes, loff_t *ppos)
{
	struct kccavs_data *data = &kccavs_test->data;
	int ret;

	/*
	 * That is what really brings the testing machine to life -- reading
	 * from the data file kicks off the cryptographic operations.
	 */
	ret = kccavs_do_calc(nbytes);
	if (ret)
		return ret;

	return simple_read_from_buffer(buf, nbytes, ppos, data->data, data->len);
}

static ssize_t kccavs_data_write(struct file *file, const char __user *buf,
				 size_t nbytes, loff_t *ppos)
{
	/*
	 * we explicitly do not clean up the cipher handle to handle MCT tests --
	 * normal KAT tests always set new keys / IVs which deallocate the
	 * handles.
	 */

	return kccavs_write_common(file, buf, nbytes, ppos, &kccavs_test->data);
}

static ssize_t kccavs_drbg_entropy_write(struct file *file,
					 const char __user *buf,
					 size_t nbytes, loff_t *ppos)
{
	return kccavs_write_common(file, buf, nbytes, ppos,
				   &kccavs_test->entropy);
}

static ssize_t kccavs_drbg_entpra_write(struct file *file,
					const char __user *buf,
					size_t nbytes, loff_t *ppos)
{
	return kccavs_write_common(file, buf, nbytes, ppos,
				   &kccavs_test->entpra);
}

static ssize_t kccavs_drbg_entprb_write(struct file *file,
					const char __user *buf,
					size_t nbytes, loff_t *ppos)
{
	return kccavs_write_common(file, buf, nbytes, ppos,
				   &kccavs_test->entprb);
}

static ssize_t kccavs_drbg_addtla_write(struct file *file,
					const char __user *buf,
					size_t nbytes, loff_t *ppos)
{
	return kccavs_write_common(file, buf, nbytes, ppos,
				   &kccavs_test->addtla);
}

static ssize_t kccavs_drbg_addtlb_write(struct file *file,
					const char __user *buf,
					size_t nbytes, loff_t *ppos)
{
	return kccavs_write_common(file, buf, nbytes, ppos,
				   &kccavs_test->addtlb);
}

static ssize_t kccavs_drbg_entropyreseed_write(struct file *file,
					       const char __user *buf,
					       size_t nbytes, loff_t *ppos)
{
	return kccavs_write_common(file, buf, nbytes, ppos,
				   &kccavs_test->entropyreseed);
}

static ssize_t kccavs_drbg_addtlreseed_write(struct file *file,
					     const char __user *buf,
					     size_t nbytes, loff_t *ppos)
{
	return kccavs_write_common(file, buf, nbytes, ppos,
				   &kccavs_test->addtlreseed);
}

static ssize_t kccavs_drbg_pers_write(struct file *file,
				      const char __user *buf,
				      size_t nbytes, loff_t *ppos)
{
	return kccavs_write_common(file, buf, nbytes, ppos, &kccavs_test->pers);
}

/* Module init: allocate memory, register the debugfs files */
static int kccavs_debugfs_init(void)
{
        kccavs_debugfs = kzalloc(sizeof(struct kccavs_debugfs), GFP_KERNEL);
	if (!kccavs_debugfs)
		return -ENOMEM;
	kccavs_debugfs->kccavs_debugfs_root =
		debugfs_create_dir(KBUILD_MODNAME, NULL);
	if (IS_ERR(kccavs_debugfs->kccavs_debugfs_root)) {
		kccavs_debugfs->kccavs_debugfs_root = NULL;
		kfree(kccavs_debugfs);
		return -1;
	}

	return 0;
}

static const struct file_operations kccavs_name_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.read = kccavs_name_read,
	.write = kccavs_name_write,
};

static const struct file_operations kccavs_key_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.read = kccavs_key_read,
	.write = kccavs_key_write,
};

static const struct file_operations kccavs_iv_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.read = kccavs_iv_read,
	.write = kccavs_iv_write,
};

static const struct file_operations kccavs_data_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.read = kccavs_data_read,
	.write = kccavs_data_write,
};

static const struct file_operations kccavs_drbg_entropy_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.write = kccavs_drbg_entropy_write,
};

static const struct file_operations kccavs_drbg_entpra_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.write = kccavs_drbg_entpra_write,
};

static const struct file_operations kccavs_drbg_entprb_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.write = kccavs_drbg_entprb_write,
};

static const struct file_operations kccavs_drbg_addtla_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.write = kccavs_drbg_addtla_write,
};

static const struct file_operations kccavs_drbg_addtlb_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.write = kccavs_drbg_addtlb_write,
};

static const struct file_operations kccavs_drbg_entropyreseed_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.write = kccavs_drbg_entropyreseed_write,
};

static const struct file_operations kccavs_drbg_addtlreseed_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.write = kccavs_drbg_addtlreseed_write,
};

static const struct file_operations kccavs_drbg_pers_fops = {
	.owner = THIS_MODULE,
	.open = simple_open,
	.write = kccavs_drbg_pers_write,
};

static int kccavs_debugfs_init_file(const char *name,
				    const struct file_operations *fops,
				    const struct dentry *dentry)
{
	dentry = debugfs_create_file(name, S_IRUSR | S_IWUSR,
				     kccavs_debugfs->kccavs_debugfs_root,
				     NULL, fops);
	if (IS_ERR(dentry)) {
		dentry = NULL;
		return -1;
	}
	return 0;
}

static int kccavs_debugfs_init_u32file(const char *name,
				       u32 *variable,
				       const struct dentry *dentry)
{
	debugfs_create_u32(name, S_IRUSR|S_IWUSR,
			   kccavs_debugfs->kccavs_debugfs_root,
			   variable);
	return 0;
}

static inline int kccavs_alloc_buffer(struct kccavs_data *buf, size_t len)
{
	if (!buf)
		return -EINVAL;

	buf->data = (char *)kzalloc(len, GFP_KERNEL);
	if (!buf->data)
		return -ENOMEM;

	buf->maxlen = len;

	return 0;
}

/*
 * XXX this can be made more dynamic in the *_write() functions
 * but then we have to think a bit about memory allocation in general to avoid
 * leaking memory
 */
static int kccavs_alloc(void)
{
	kccavs_test = kzalloc(sizeof(struct kccavs_test), GFP_KERNEL);
	if (!kccavs_test)
		return -ENOMEM;
	if (kccavs_alloc_buffer(&kccavs_test->key, MAXDATALEN))
		goto freeapi;
	if (kccavs_alloc_buffer(&kccavs_test->data, MAXDATALEN))
		goto freekey;
	if (kccavs_alloc_buffer(&kccavs_test->iv, MAXLEN))
		goto freedata;
	if (kccavs_alloc_buffer(&kccavs_test->entropy, MAXLEN))
		goto freeiv;
	if (kccavs_alloc_buffer(&kccavs_test->entpra, MAXLEN))
		goto freeentropy;
	if (kccavs_alloc_buffer(&kccavs_test->entprb, MAXLEN))
		goto freeentpra;
	if (kccavs_alloc_buffer(&kccavs_test->addtla, MAXLEN))
		goto freeentprb;
	if (kccavs_alloc_buffer(&kccavs_test->addtlb, MAXLEN))
		goto freeaddtla;
	if (kccavs_alloc_buffer(&kccavs_test->entropyreseed, MAXLEN))
		goto freeaddtlb;
	if (kccavs_alloc_buffer(&kccavs_test->addtlreseed, MAXLEN))
		goto freeentropyreseed;
	if (kccavs_alloc_buffer(&kccavs_test->pers, MAXLEN))
		goto freeaddtlreseed;

	return 0;

freeaddtlreseed:
	kfree(kccavs_test->addtlreseed.data);
freeentropyreseed:
	kfree(kccavs_test->entropyreseed.data);
freeaddtlb:
	kfree(kccavs_test->addtlb.data);
freeaddtla:
	kfree(kccavs_test->addtla.data);
freeentprb:
	kfree(kccavs_test->entprb.data);
freeentpra:
	kfree(kccavs_test->entpra.data);
freeentropy:
	kfree(kccavs_test->entropy.data);
freeiv:
	kfree(kccavs_test->iv.data);
freedata:
	kfree(kccavs_test->data.data);
freekey:
	kfree(kccavs_test->key.data);
freeapi:
	kfree(kccavs_test);
	return -ENOMEM;
}

static void kccavs_dealloc_data(struct kccavs_data *data)
{
	kfree(data->data);
	data->data = NULL;
}
static void kccavs_dealloc(void)
{
	kccavs_dealloc_data(&kccavs_test->key);
	kccavs_dealloc_data(&kccavs_test->data);
	kccavs_dealloc_data(&kccavs_test->iv);
	kccavs_dealloc_data(&kccavs_test->entropy);
	kccavs_dealloc_data(&kccavs_test->entpra);
	kccavs_dealloc_data(&kccavs_test->entprb);
	kccavs_dealloc_data(&kccavs_test->addtla);
	kccavs_dealloc_data(&kccavs_test->addtlb);
	kccavs_dealloc_data(&kccavs_test->entropyreseed);
	kccavs_dealloc_data(&kccavs_test->addtlreseed);
	kccavs_dealloc_data(&kccavs_test->pers);

	kccavs_free_cipher();

	kfree(kccavs_test);
}

static int __init kccavs_init(void)
{
	int ret;

	ret = kccavs_alloc();
	if (ret)
		return ret;
	kccavs_scrub();

	ret = -EINVAL;
	if (kccavs_debugfs_init() < 0)
		goto out;
	if (kccavs_debugfs_init_u32file("type", &kccavs_test->type,
				kccavs_debugfs->kccavs_debugfs_type) < 0)
		goto outfs;
	if (kccavs_debugfs_init_u32file("keylen", &kccavs_test->keylen,
				kccavs_debugfs->kccavs_debugfs_keylen) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("key", &kccavs_key_fops,
				     kccavs_debugfs->kccavs_debugfs_key) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("data", &kccavs_data_fops,
				     kccavs_debugfs->kccavs_debugfs_data) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("iv", &kccavs_iv_fops,
				     kccavs_debugfs->kccavs_debugfs_iv) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("name", &kccavs_name_fops,
				     kccavs_debugfs->kccavs_debugfs_name) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("drbg_entropy", &kccavs_drbg_entropy_fops,
			kccavs_debugfs->kccavs_debugfs_drbg_entropy) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("drbg_entpra", &kccavs_drbg_entpra_fops,
			kccavs_debugfs->kccavs_debugfs_drbg_entpra) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("drbg_entprb", &kccavs_drbg_entprb_fops,
			kccavs_debugfs->kccavs_debugfs_drbg_entprb) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("drbg_addtla", &kccavs_drbg_addtla_fops,
			kccavs_debugfs->kccavs_debugfs_drbg_addtla) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("drbg_addtlb", &kccavs_drbg_addtlb_fops,
			kccavs_debugfs->kccavs_debugfs_drbg_addtlb) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("drbg_entropyreseed",
				     &kccavs_drbg_entropyreseed_fops,
			kccavs_debugfs->kccavs_debugfs_drbg_entropyreseed) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("drbg_addtlreseed",
				     &kccavs_drbg_addtlreseed_fops,
			kccavs_debugfs->kccavs_debugfs_drbg_addtlreseed) < 0)
		goto outfs;
	if (kccavs_debugfs_init_file("drbg_pers", &kccavs_drbg_pers_fops,
				kccavs_debugfs->kccavs_debugfs_drbg_pers) < 0)
		goto outfs;

        return 0;

outfs:
	debugfs_remove_recursive(kccavs_debugfs->kccavs_debugfs_root);
out:
	kccavs_dealloc();
	return ret;
}

static void __exit kccavs_exit(void)
{
	debugfs_remove_recursive(kccavs_debugfs->kccavs_debugfs_root);
	kccavs_scrub();
	kccavs_dealloc();
}

module_init(kccavs_init);
module_exit(kccavs_exit);
