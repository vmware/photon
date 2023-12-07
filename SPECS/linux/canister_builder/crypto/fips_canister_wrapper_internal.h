/*
 * Kernel APIs called by canister wrapper.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */

#include <linux/scatterlist.h>

/* Testmgr structures and enums */
/*
 * Need slab memory for testing (size in number of pages).
 */
#define XBUFSIZE	8

#define TEST_SG_TOTAL	10000

#define TESTMGR_POISON_BYTE	0xfe
#define TESTMGR_POISON_LEN	16

/* flush type for hash algorithms */
enum flush_type {
	/* merge with update of previous buffer(s) */
	FLUSH_TYPE_NONE = 0,

	/* update with previous buffer(s) before doing this one */
	FLUSH_TYPE_FLUSH,

	/* likewise, but also export and re-import the intermediate state */
	FLUSH_TYPE_REIMPORT,
};

/* finalization function for hash algorithms */
enum finalization_type {
	FINALIZATION_TYPE_FINAL,	/* use final() */
	FINALIZATION_TYPE_FINUP,	/* use finup() */
	FINALIZATION_TYPE_DIGEST,	/* use digest() */
};

/*
 * Whether the crypto operation will occur in-place, and if so whether the
 * source and destination scatterlist pointers will coincide (req->src ==
 * req->dst), or whether they'll merely point to two separate scatterlists
 * (req->src != req->dst) that reference the same underlying memory.
 *
 * This is only relevant for algorithm types that support in-place operation.
 */
enum inplace_mode {
	OUT_OF_PLACE,
	INPLACE_ONE_SGLIST,
	INPLACE_TWO_SGLISTS,
};

/**
 * struct test_sg_division - description of a scatterlist entry
 *
 * This struct describes one entry of a scatterlist being constructed to check a
 * crypto test vector.
 *
 * @proportion_of_total: length of this chunk relative to the total length,
 *			 given as a proportion out of TEST_SG_TOTAL so that it
 *			 scales to fit any test vector
 * @offset: byte offset into a 2-page buffer at which this chunk will start
 * @offset_relative_to_alignmask: if true, add the algorithm's alignmask to the
 *				  @offset
 * @flush_type: for hashes, whether an update() should be done now vs.
 *		continuing to accumulate data
 * @nosimd: if doing the pending update(), do it with SIMD disabled?
 */
struct test_sg_division {
	unsigned int proportion_of_total;
	unsigned int offset;
	bool offset_relative_to_alignmask;
	enum flush_type flush_type;
	bool nosimd;
};

struct test_sglist {
	char *bufs[XBUFSIZE];
	struct scatterlist sgl[XBUFSIZE];
	struct scatterlist sgl_saved[XBUFSIZE];
	struct scatterlist *sgl_ptr;
	unsigned int nents;
};

struct cipher_test_sglists {
	struct test_sglist src;
	struct test_sglist dst;
};

/**
 * struct testvec_config - configuration for testing a crypto test vector
 *
 * This struct describes the data layout and other parameters with which each
 * crypto test vector can be tested.
 *
 * @name: name of this config, logged for debugging purposes if a test fails
 * @inplace_mode: whether and how to operate on the data in-place, if applicable
 * @req_flags: extra request_flags, e.g. CRYPTO_TFM_REQ_MAY_SLEEP
 * @src_divs: description of how to arrange the source scatterlist
 * @dst_divs: description of how to arrange the dst scatterlist, if applicable
 *	      for the algorithm type.  Defaults to @src_divs if unset.
 * @iv_offset: misalignment of the IV in the range [0..MAX_ALGAPI_ALIGNMASK+1],
 *	       where 0 is aligned to a 2*(MAX_ALGAPI_ALIGNMASK+1) byte boundary
 * @iv_offset_relative_to_alignmask: if true, add the algorithm's alignmask to
 *				     the @iv_offset
 * @key_offset: misalignment of the key, where 0 is default alignment
 * @key_offset_relative_to_alignmask: if true, add the algorithm's alignmask to
 *				      the @key_offset
 * @finalization_type: what finalization function to use for hashes
 * @nosimd: execute with SIMD disabled?  Requires !CRYPTO_TFM_REQ_MAY_SLEEP.
 */
struct testvec_config {
	const char *name;
	enum inplace_mode inplace_mode;
	u32 req_flags;
	struct test_sg_division src_divs[XBUFSIZE];
	struct test_sg_division dst_divs[XBUFSIZE];
	unsigned int iv_offset;
	unsigned int key_offset;
	bool iv_offset_relative_to_alignmask;
	bool key_offset_relative_to_alignmask;
	enum finalization_type finalization_type;
	bool nosimd;
};

/*
 * hash_testvec:	structure to describe a hash (message digest) test
 * @key:	Pointer to key (NULL if none)
 * @plaintext:	Pointer to source data
 * @digest:	Pointer to expected digest
 * @psize:	Length of source data in bytes
 * @ksize:	Length of @key in bytes (0 if no key)
 * @setkey_error: Expected error from setkey()
 * @digest_error: Expected error from digest()
 * @fips_skip:	Skip the test vector in FIPS mode
 */
struct hash_testvec {
	const char *key;
	const char *plaintext;
	const char *digest;
	unsigned int psize;
	unsigned short ksize;
	int setkey_error;
	int digest_error;
	bool fips_skip;
};

extern int fips_integrity_check (void);
extern int crypto_self_test_init(void);
extern int cryptomgr_init(void);
extern int hmac_module_init(void);
extern int crypto_cbc_module_init(void);
extern int crypto_cfb_module_init(void);
extern int crypto_ccm_module_init(void);
extern int crypto_gcm_module_init(void);
extern int aes_init(void);
extern int drbg_init(void);
extern int xts_module_init(void);
extern int sha1_generic_mod_init(void);
extern int sha256_generic_mod_init(void);
extern int sha512_generic_mod_init(void);
extern int rsa_init(void);
extern int ecdsa_init(void);
extern int ecdh_init(void);
extern int crypto_ecb_module_init(void);
extern int crypto_cts_module_init(void);
extern int crypto_ctr_module_init(void);
extern int crypto_cmac_module_init(void);
extern int aesni_init(void);
extern void cryptomgr_exit(void);
extern void crypto_cbc_module_exit(void);
extern void crypto_ccm_module_exit(void);
extern void crypto_cfb_module_exit(void);
extern void crypto_cmac_module_exit(void);
extern void crypto_ctr_module_exit(void);
extern void crypto_cts_module_exit(void);
extern void drbg_exit(void);
extern void crypto_ecb_module_exit(void);
extern void ecdh_exit(void);
extern void ecdsa_exit(void);
extern void crypto_gcm_module_exit(void);
extern void hmac_module_exit(void);
extern void rsa_exit(void);
extern void sha1_generic_mod_fini(void);
extern void sha256_generic_mod_fini(void);
extern void sha512_generic_mod_fini(void);
extern void xts_module_exit(void);
extern void aesni_exit(void);
extern void aes_fini(void);
extern int __init dh_init(void);
extern void __exit dh_exit(void);
extern int __init sha3_generic_mod_init(void);
extern void __exit sha3_generic_mod_fini(void);
extern int seqiv_module_init(void);
extern void seqiv_module_exit(void);
extern int __init ghash_mod_init(void);
extern void __exit ghash_mod_exit(void);
