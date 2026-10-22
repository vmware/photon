echo "Check for .config applicability"

# make doesn't support _smp_mflags
make LC_ALL= olddefconfig

# Remove comment with a version string
sed -i '3d' .config

# Check for known acvp diff, else return error
ignore_list="CONFIG_CRYPTO_USER_API_AKCIPHER\|CONFIG_CRYPTO_USER_API_KPP\|CONFIG_CRYPTO_USER_API_ECC"
diff -u .config.old .config -I "$ignore_list"

# Apply config changes for ACVP Build
./scripts/kconfig/merge_config.sh .config .config_acvp
./scripts/kconfig/merge_config.sh -s -m .config .config_acvp
sed -i '3d' .config
