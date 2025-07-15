#!/bin/bash

dbg_funcs=(
	"crypto_aead_setkey"
	"crypto_aead_setauthsize"
	"crypto_aead_encrypt"
	"crypto_aead_decrypt"
	"crypto_aead_init_tfm"
	"ahash_restore_req"
	"crypto_akcipher_init_tfm"
	"ecc_sendmsg"
	"ecc_recvmsg"
	"crypto_cipher_setkey"
	"crypto_kpp_init_tfm"
	"crypto_rng_reset"
	"crypto_shash_update"
	"crypto_shash_setkey"
	"crypto_shash_init_tfm"
	"crypto_shash_final"
	"crypto_skcipher_setkey"
	"crypto_skcipher_encrypt"
	"crypto_skcipher_decrypt"
	"crypto_skcipher_init_tfm"
)

_prefix=
_p=

if [[ "$1" == "enable" ]]; then
	_prefix="En"
	_p="+p"
elif [[ "$1" == "disable" ]]; then
	_prefix="Dis"
	_p="-p"
else
	echo "Unknown option: $1"
	echo "Acceptable options: 'enable' or 'disable'"
	exit 1
fi

for func in "${dbg_funcs[@]}"; do
	echo "${_prefix}abling debug prints for $func"
	echo "func "$func" $_p" > /proc/dynamic_debug/control
done
