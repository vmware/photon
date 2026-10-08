/*
 * canister functions invoked from wrapper layer.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */

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
