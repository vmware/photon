%define __modules_gen_hmac \
MODULES="aes-x86_64 aesni-intel authenc cryptd crypto_null ctr seqiv sha512_generic tcrypt lrw xts ecb cbc des_generic sha256_generic algif_skcipher ccm cmac gcm lzo ghash-generic jitterentropy_rng drbg ecdh_generic hmac_generator" \
KEY="FIPS-PH3-VMW2020" \
for MODULE in $MODULES ;do \
FULL_PATH=`find %{buildroot}/lib/modules/. -name "$MODULE.ko.xz"` \
if [ ! -z  "$FULL_PATH" ] \
then \
DIRECTORY=$(dirname $FULL_PATH) \
FILENAME=$(basename $FULL_PATH) \
openssl dgst -sha256 -hmac "$KEY" "$FULL_PATH" > $DIRECTORY/.$FILENAME.hmac \
fi \
done \
VMLINUZ_PATH=%{buildroot}/boot/vmlinuz-%{uname_r}  \
openssl dgst -sha256 -hmac "$KEY" "$VMLINUZ_PATH" > %{buildroot}/boot/.vmlinuz-%{uname_r}.hmac \
%{nil}
