%dnl Shared canister/.config manipulation for the Photon kernel flavours.
%dnl
%dnl Included by both SPECS/linux/linux.spec and SPECS/linux/linux-esx.spec so
%dnl that the FIPS canister Kconfig handling cannot diverge between the two
%dnl flavours again. Historically linux.spec had no fips=0 branch at all, so on
%dnl aarch64 (fips=0) the canister "is not set" comments were left in .config;
%dnl "make olddefconfig" silently drops symbols that do not exist in the tree
%dnl and the check_for_config_applicability.inc diff guard then failed.
%dnl
%dnl Expects, from the including spec:
%dnl   fips           1 => build a FIPS kernel carrying the crypto canister
%dnl   canister_build 1 => the canister is built from source in this build
%dnl   canister_usage 1 => link against a prebuilt canister object file
%dnl                       (derived: !canister_build when fips=1, else 0)
%dnl
%dnl Expects .config to be in place already (cp of the flavour config Source).
%dnl
%dnl The GCC_PLUGIN_MATCH_CANISTER_STRUCTS / GCC_PLUGIN_PAD_CANISTER_STRUCTS
%dnl Kconfig symbols only exist once the fips canister plugin patches have been
%dnl applied, i.e. only when fips=1.
%if 0%{?canister_build}
sed -i "s/# CONFIG_GCC_PLUGIN_PAD_CANISTER_STRUCTS is not set/CONFIG_GCC_PLUGIN_PAD_CANISTER_STRUCTS=y/" .config
sed -i "/# CONFIG_GCC_PLUGIN_MATCH_CANISTER_STRUCTS is not set/d" .config
%endif

%if 0%{?canister_usage}
sed -i "s/# CONFIG_GCC_PLUGIN_MATCH_CANISTER_STRUCTS is not set/CONFIG_GCC_PLUGIN_MATCH_CANISTER_STRUCTS=y/" .config
%endif

%if 0%{?fips} == 0
# Clean up .config of FIPS related configs
sed -i "/# CONFIG_GCC_PLUGIN_MATCH_CANISTER_STRUCTS is not set/d" .config
sed -i "/# CONFIG_GCC_PLUGIN_PAD_CANISTER_STRUCTS is not set/d" .config
%endif
