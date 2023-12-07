/*
 * canister functions invoked from wrapper layer.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Author: Keerthana K <keerthanak@vmware.com>
 *
 */

#include <linux/module.h>
#include "fips_canister_wrapper_internal.h"

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
	seqiv_module_init();
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
	seqiv_module_exit();
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
