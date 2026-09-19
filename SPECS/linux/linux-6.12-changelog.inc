%changelog
* Sat Sep 19 2026 Daniel Casota <dcasota@gmail.com> 6.12.109-7
- Share canister/.config handling via canister_config.inc (fixes the fips=0 path) and make canister_build work against the current kernel
* Fri Sep 18 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.109-6
- Fixes CVE-2026-68337, CVE-2026-68441
* Thu Sep 17 2026 srinidhira0 <srinidhi.rao@broadcom.com> 6.12.109-5
- Fixes CVE-2026-43464, CVE-2026-45932, CVE-2026-46324, CVE-2026-52956
* Wed Sep 16 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.12.109-4
- Fix rpm build warnings
- Exclude bpf_jit_disasm binary to avoid binutils-libs dependency
* Wed Sep 16 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.109-3
- Fixes CVE-2026-80785
* Tue Sep 15 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.109-2
- Fixes CVE-2026-74605, CVE-2026-74611
* Fri Sep 11 2026 Ajay Kaher <ajay.kaher@broadcom.com> 6.12.109-1
- Update to version 6.12.109
* Fri Sep 11 2026 Ajay Kaher <ajay.kaher@broadcom.com> 6.12.107-11
- Fixes CVE-2026-68399, CVE-2026-68404, CVE-2026-68409, CVE-2026-68441, CVE-2026-68447, CVE-2026-74571
* Thu Sep 10 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.107-10
- version bump to build along with sysdig and falco
* Thu Sep 10 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.107-9
- Fixes CVE-2026-74571, CVE-2026-80580
* Tue Sep 08 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.107-8
- Fixes CVE-2026-63853, CVE-2026-63879, CVE-2026-64036, CVE-2026-64058, CVE-2026-64078
* Tue Sep 08 2026 srinidhira0 <srinidhi.rao@broadcom.com> 6.12.107-7
- Fixes CVE-2026-64160
* Tue Sep 08 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.107-6
- Fixes CVE-2026-72366, CVE-2026-72463, CVE-2026-72493, CVE-2026-74268, CVE-2026-74269
* Tue Sep 08 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.107-5
- Fixes CVE-2026-72413, CVE-2026-72423
* Mon Sep 07 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.107-4
- Fixes CVE-2026-72288, CVE-2026-72355
* Wed Sep 02 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.107-3
- sched_info_enqueue: don't update last_queued on delayed migration
* Tue Sep 01 2026 Bo Gan <bo.gan@broadcom.com> 6.12.107-2
- Backport upstream fix to solve ACPI PNP0C01/PNP0C02 device registration with platform driver
* Mon Aug 31 2026 Ajay Kaher <ajay.kaher@broadcom.com> 6.12.107-1
- Update to version 6.12.107
* Mon Aug 31 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.103-11
- Rebased acvp patches for linux-6.12.10*
* Mon Aug 31 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.103-10
- Fix CVE-2026-68082
* Tue Aug 25 2026 Ajay Kaher <ajay.kaher@broadcom.com> 6.12.103-9
- Fixes CVEs
* Tue Aug 25 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.103-8
- Fixes CVE-2026-63979, CVE-2026-64024, CVE-2026-64066, CVE-2026-64067, CVE-2026-64068
* Fri Aug 21 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.103-7
- Make ima module to use lib sha1 instead of crypto shash
* Thu Aug 20 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.12.103-6
- Remove linux requires from linux-tools
- Users are expected to handle that part if there is a mismatch between tools and kernel
* Wed Aug 19 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.103-5
- Remove selinux=0 from default cmdline; SELinux is now disabled via selinux-policy
* Mon Aug 17 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.103-4
- rap_plugin: fix function alignment gap and tighten caller-side check to match KCFI
- Update canister v6.12.60-18.2 with rap_plugin function alignment gap fix
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.103-3
- Extend to build for 91 and above
* Thu Aug 13 2026 srinidhira0 <srinidhi.rao@broadcom.com> 6.12.103-2
- Fixes CVE-2026-52988, CVE-2026-52991, CVE-2026-53089, CVE-2026-53091
* Mon Aug 10 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.12.103-1
- Update to version 6.12.103
* Thu Aug 06 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.96-9
- Make SELinux opt-in by default (add selinux=0 to default cmdline)
* Thu Aug 06 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.96-8
- Rebased acvp patches for linux-6.12.9*
* Wed Aug 05 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.12.96-7
- Fixes CVE-2025-40158, CVE-2025-68745, CVE-2026-63872, CVE-2026-64076, CVE-2026-64077
* Mon Aug 03 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.96-6
- Fixes CVE-2025-40074, CVE-2025-68353, CVE-2026-23208, CVE-2026-43009, CVE-2026-43485
* Thu Jul 30 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.96-5
- Update canister v6.12.60-18.1 with CVE-2026-64313 fix
* Thu Jul 30 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.96-4
- Fixes CVE-2026-43197, CVE-2026-43198
* Tue Jul 28 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.96-3
- Backport upstream randomize_kstack: Unify random source across arches
- (a96ef5848cb0).
* Mon Jul 27 2026 Ajay Kaher <ajay.kaher@broadcom.com> 6.12.96-2
- Fixes CVE-2026-31589, CVE-2026-43414, CVE-2026-43465, CVE-2026-53224, CVE-2026-53246, CVE-2026-53260
* Mon Jul 20 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.12.96-1
- Update to version 6.12.96
* Tue Jul 07 2026 Bo Gan <bo.gan@broadcom.com> 6.12.95-2
- Fix for vmxnet3 BUG_ON in vmxnet3_get_hdr_len()
* Mon Jul 06 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.12.95-1
- Update to version 6.12.95
* Mon Jun 22 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.12.94-1
- Update to version 6.12.94
* Sat Jun 20 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.12.92-3
- Add mpc-devel to build requires
* Thu Jun 04 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.92-2
- Consolidate CVE patches into kernel_cve_patches.inc (range 3000-3999)
* Tue Jun 02 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.92-1
- Update to version 6.12.92
- Fix CVE-2025-68359 and CVE-2026-43101
- sshedi: fix vmlinux exclusion issue from debuginfo rpm
* Tue May 19 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.87-2
- Fix CVE-2026-43083
* Mon May 11 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.87-1
- Update to version 6.12.87
* Tue May 05 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.78-5
- Moved SPECS/linux/v6.12(common branch) to SPECS/linux(5.0 branch)
- Used merge commit to keep the history in 5.0 itself
* Mon Apr 27 2026 Ajay Kaher <ajay.kaher@broadcom.com> 6.12.78-4
- Disable CONFIG_PER_VMA_LOCK
* Fri Apr 10 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.78-3
- Drop unused HCX patches
* Sun Apr 05 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.78-2
- Fix linux-tools build with newer glibc
* Thu Mar 26 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.78-1
- Update to version 6.12.78
* Mon Mar 16 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.69-7
- SELinux as a default LSM
- Add erofs support
- Enable CONFIG_NF_FLOW_TABLE=m
* Mon Mar 09 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.69-6
- Fix af_unix boolean registration from the wrong array to the correct one
* Wed Mar 04 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.69-5
- HCX: Update enums to higher value to avoid UAPI conflict with new kernel features
* Mon Mar 02 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.69-4
- Fix aarch64 build
* Thu Feb 26 2026 Bo Gan <bo.gan@broadcom.com> 6.12.69-3
- Enable MEMCG_V1 and CPUSETS_V1 for other flavors as generic/x86 does
* Fri Feb 20 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.69-2
- Support steal clock on TDX enabled VMs
* Fri Feb 20 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.69-1
- Update to version 6.12.69
* Wed Feb 18 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.60-22
- Disable Bluetooth and CAN support
- Fix requires on doc sub package
* Wed Feb 11 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.60-21
- Port ARM patches to v6.12 and include new patch for reporting guest crashes
- the VMware hypervisor
* Tue Feb 10 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.60-20
- HCX patches ported to 6.12 kernel
* Fri Feb 06 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.60-19
- Update canister version to 6.12.60-18
* Thu Feb 05 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.60-18
- Improve FIPS canister matching plugin
* Tue Feb 03 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.60-17
- Add viomem kernel module
* Tue Feb 03 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.60-16
- Track internal/external requests to jitterentropy
* Mon Feb 02 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.60-15
- Enable CONFIG_TDX_GUEST_DRIVER required for CoCo.
* Thu Jan 22 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.60-14
- Update canister version to 6.12.60-13
* Thu Jan 15 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.60-13
- .config: added security hardened changes.
- canister_build: official build of the canister to include previous fix.
* Mon Jan 12 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.60-12
- canister_build: Fix UAF (req->iv) in seqiv
* Wed Jan 07 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.60-11
- Update jitterentropy driver names in canister_algs list
* Sat Jan 03 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.60-10
- Introduce /sys/kernel/vmgenid
* Fri Jan 02 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.60-9
- Enable CONFIG_NFT_FIB_IPV4 and CONFIG_NFT_FIB_IPV6
* Mon Dec 29 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.60-8
- Disable CONFIG_GCC_PLUGIN_LATENT_ENTROPY
* Mon Dec 22 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.12.60-7
- Fix SBAT validation order
* Fri Dec 19 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.60-6
- Disable unique naming for *.ko.debug to make crash utility happy
* Fri Dec 12 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.12.60-5
- Inject photon KM certificate to trusted keyring
* Fri Dec 12 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.60-4
- Consuming canister.
* Thu Dec 11 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.60-3
- Remove module.h and other related metadata from aes/sha256.c
* Thu Dec 04 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.60-2
- Enable CONFIG_ARM64_ERRATUM_3194386
* Thu Dec 04 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.60-1
- Update to version 6.12.60.
* Wed Dec 03 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.57-9
- canister: Move out lib/crypto/{mpi/memneq/utils/gf128mul} of boundry
* Mon Dec 01 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.57-8
- Enable CONFIG_GVE for gVNIC support
* Mon Dec 01 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.57-7
- Add VAES based alsos to canister approved list.
* Tue Nov 25 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.57-6
- Add kat_build flag for CMVP demo, Remove patch for allow external IVs for ACVP
* Tue Nov 25 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.57-5
- Keep .BTF section in kernel modules
* Mon Nov 24 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.57-4
- Revert: canister: adding asn1_decoder library
* Fri Nov 14 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.57-3
- Add jitterentropy_rng_proxy
* Thu Nov 13 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.57-2
- Make lib/digsig to use lib SHA1 instead of crypto shash API
* Tue Nov 11 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.57-1
- Update to version 6.12.57
* Tue Nov 11 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.41-24
- Removed '__SCT__cond_resched' symbol from canister
* Thu Nov 06 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.41-23
- Introduce new printk wrapper for FIPS canister.
* Thu Oct 30 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.41-22
- Moving rfc4543 of gcm out of canister boundry.
- Removed all approved/non-approved log indicators.
* Mon Oct 27 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-21
- Consume a canister binary via RPM dependency
* Fri Oct 24 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.12.41-20
- perf: add patch to collect off-cpu sample
* Mon Oct 13 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.41-19
- Moving asn1-decoder API into canister boundry.
- Restore rsa-pkcs1pad encrypt/decrypt in rsa-pkcs1pad.c, disallow in fips mode
- Make sha1 combinations as fips_allowed=0 for self-test
* Mon Oct 06 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-18
- Canister: use __NO_FORTIFY and use memcpy as is
* Tue Sep 30 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-17
- Cleanup canister usage/build patch sets
* Tue Sep 30 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-16
- fips-canister: go back to tarball as the only way to preserve unstripped
  fips_canister.o
* Mon Sep 29 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.41-15
- Moving MPI library API inside canister
* Mon Sep 29 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.41-14
- crypto: zero initialize memory allocated via sock_kmalloc
* Fri Sep 26 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-13
- fips-canister: prepare for RPM consumption instead of a tarball
* Fri Sep 26 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-12
- Canister: Perform partial relocation for local symbols
* Mon Sep 22 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.41-11
- Totally block external IVs for gcm(aes)
* Thu Sep 18 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.12.41-10
- Fixes for vmwnet3 driver
* Wed Sep 17 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-9
- Canister: Move crypto_inc to lib/crypto/utils.c
* Wed Sep 17 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-8
- Canister: Move shasum helpers to the canister
* Thu Sep 11 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.41-7
- Select jitterentropy mem size as 32KB
- Disable jent_loop_shuffle in Jitterentropy.
- Add support for OSR(max) calculation.
* Thu Sep 11 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-6
- Canister: Add ghasg accelerator and lib/crypto utils
- Canister: fix shasum accelerators inclusion
- Canister: creation and integrity ehnancements
* Wed Sep 10 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-5
- Canister: introduce straight-line-speculation mitigation
* Mon Sep 08 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.41-4
- Resolve random EBUSY status for RSA signature verification test
* Mon Aug 25 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.41-3
- Removed rsa, cfb(aes) and added ecdsa-nist-p521 to tamper alg_list,
- Added HMAC and HASH DRBGs using SHA-384 in FIPS mode
* Thu Aug 21 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.41-2
- Add shasums accelerators
- Speedup algos registration in non-FIPS mode
* Thu Aug 14 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.41-1
- Update to version 6.12.41
* Tue Aug 5 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.34-9
- Convert ACVP printk to pr_debug
* Mon Jul 28 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.34-8
- Convert canister structure spinlock fields to static memory
* Thu Jul 24 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.34-7
- Fix KAT build
- Spec clean up around fips macros
* Fri Jul 18 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.34-6
- Add sample collection support for Jitterentropy.
* Wed Jul 16 2025 Brennan Lamoreaux <brenna.lamoreaux@broadcom.com> 6.12.34-5
- Implement structure member type check within GCC plugins. Obsoletes
- old structure comparator test.
* Tue Jul 15 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.34-4
- linux: Use canister 6.12.34-3
* Fri Jul 11 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.34-3
- Pending ECB move changes
* Thu Jul 03 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.12.34-2
- Move ecb out of canister
- Clean up and reorder SREL type & addon combinations
- Add readline-devel as a build requirement for tools
* Fri Jun 27 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.34-1
- Upgrade linux kernel to version 6.12.34.
* Wed Jun 25 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.1-19
- linux: Use canister version 6.12.1-18.ph5
* Tue Jun 17 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.1-18
- Move sha1 functions out of canister boundry
- Do not register sha1 to crypt api when fips is enabled
* Fri Jun 13 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.12.1-17
- Introduce FIPS canister plugins
* Tue Jun 03 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.1-16
- Changes to Jitterentropy.
* Thu May 15 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.1-15
- Moved 'x86_cpu_id' struct access to fips canister wrapper
- Disable alloc_hook_tags if MEM_PROFILING is disabled
* Sat May 10 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.12.1-14
- Require coreutils and remove xml-security-c-devel from build requires
* Wed Apr 30 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.12.1-13
- Move rsa-pkcs1pad encrypt/decrypt functions out of canister boundry
- Fail rsa-pkcs1pad encrypt/decrypt in fips mode
- Use version-release for canister version, remove 6.0.0
* Tue Apr 22 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.1-12
- Update canister binary v6.12.1-11
* Thu Apr 17 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.1-11
- Remove essIV and echainIV from canister
* Tue Mar 25 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.12.1-10
- Sign kernel module using SHA3-512 hash algo
* Thu Mar 20 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.12.1-9
- Include SBAT and kexec patches
* Wed Mar 19 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.1-8
- Enable hmac(sha384) self-test
* Thu Mar 13 2025 Mukul Sikka <mukul.sikka@broadcom.com> 6.12.1-7
- Release bump for SRP compliance
* Mon Mar 03 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.12.1-6
- Fix build error in acvp build and some spec refinement
* Mon Feb 24 2025 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.1-5
- Update fips canister to version 6.0.0-6.12.1-4
- Improve fips canister struct definition check
* Mon Feb 24 2025 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.1-4
- Add Support for essiv echainiv in canister
* Mon Feb 24 2025 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.12.1-3
- Canister build for v6.12.x
* Thu Feb 20 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.1-2
- Enable cgroup_v1 support for mem & cpuset control groups.
* Tue Feb 04 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.12.1-1
- Upgrade to version 6.12.x.
* Thu Sep 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.6.28-2
- Fix backward compatibility issue
* Thu Aug 29 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.6.28-1
- Upgrade to version 6.6.x.
* Fri May 17 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.83-6
- Re-enable CONFIG_SECURITY_SELINUX_DEVELOP to fix boot time regressions
  in stig hardened systems.
* Fri May 17 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.83-5
- linux-generic will now obsolete and provide linux-secure as linux-secure
  has been merged into linux-generic. This will ensure tdnf update on
  Photon 5.0 is handled gracefully.
* Mon Apr 29 2024 Roye Eshed <roye.eshed@broadcom.com> 6.1.83-4
- Fix for CVE-2023-52586 by disabling CONFIG_DRM_MSM
* Mon Apr 29 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.83-3
- Enable CONFIG_ATA_PIIX for ata/pata intel SFF drivers replacing legacy IDE drivers
* Mon Apr 29 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.83-2
- Patched CVE-2024-26643
* Mon Apr 29 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.83-1
- Update to version 6.1.83
- Fix CVE-2024-26642
* Mon Apr 29 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.81-5
- Update SBAT verification
* Mon Apr 29 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.81-4
- Fix CVE-2024-52452
* Mon Apr 29 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.81-3
- Fix CVE-2023-52585
* Mon Apr 29 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.81-2
- Patched CVE-2024-26585
* Mon Apr 29 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.81-1
- Update to version 6.1.81, patched CVE-2024-26584
* Mon Apr 29 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.79-2
- Fixes CVE-2024-23307 and CVE-2024-22099
* Mon Apr 29 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.79-1
- Update to version 6.1.79
* Mon Apr 29 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.77-1
- Update to version 6.1.77
* Mon Apr 29 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.75-1
- Update to version 6.1.75
* Mon Apr 29 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.70-6
- Fix CVE-2023-6915
* Mon Apr 29 2024 Bryan Tan <bryan-bt.tan@broadcom.com> 6.1.70-5
- Fix refcount underflow in vsock
* Mon Apr 29 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.70-4
- Fix CVE-2024-0340
* Mon Apr 29 2024 Kuntal Nayak <nkuntal@vmware.com> 6.1.70-3
- Fix CVE-2023-39191
* Mon Apr 29 2024 Kuntal Nayak <nkuntal@vmware.com> 6.1.70-2
- Fix CVE-2023-5633
* Mon Apr 29 2024 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.70-1
- Update to version 6.1.70
* Mon Apr 29 2024 Srish Srinivasan <ssrish@vmware.com> 6.1.62-13
- print kernel crypto API return status for LKCM5 demo
- move all the ACVP related patches under a dedicated directory called
  acvp_patches
* Mon Apr 22 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.62-12
- Port secure kernel changes to generic
* Tue Mar 26 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 6.1.62-11
- Fix proc_sched_rt01 ltp testcase failure
* Mon Feb 12 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.62-10
- Update canister version to 5.0.0-6.1.75-2
* Fri Feb 02 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.62-9
- Enable CONFIG_PROC_EVENTS
* Wed Dec 20 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-8
- Update canister to 5.0.0-6.1.62-13
* Wed Dec 20 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-7
- FIPS: Add log messages for approved and non-approved services
- Remove fips=2 logic
* Wed Dec 20 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-6
- Added self-tests for rsa-pkcs1pad in combination with sha1, sha224, sha384 and sha512
* Wed Dec 20 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-5
- Update canister to 5.0.0-6.1.62-7
* Wed Dec 20 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-4
- Update canister to 5.0.0-6.1.62-2
* Wed Dec 20 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-3
- Fix RSA self tests
* Wed Nov 29 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.62-2
- Fix for CVE-2023-2176
* Wed Nov 29 2023 Ankit Jain <ankitja@vmware.com> 6.1.62-1
- Update to version 6.1.62
* Wed Nov 29 2023 Ankit Jain <ankitja@vmware.com> 6.1.60-4
- Fix for CVE-2023-0597
* Wed Nov 29 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.60-3
- Remove kat_build and its associated spec changes
* Wed Nov 29 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.60-2
- Jitterentropy sample collection support in ACVP Build.
* Wed Nov 29 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.60-1
- Upgrade to 6.1.60
* Wed Nov 29 2023 Alexey Makhalov <amakhalov@vmware.com> 6.1.56-9
- Add .sbat section for bzImage
- Introduce SBAT verificaion in addition to signature on kexec
* Wed Nov 29 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-8
- Upgrade canister to 5.0.0-6.1.56-6
* Wed Nov 29 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-7
- Added cts to crypto self-tests
- Removed rsa(pkcs1pad, sha256), rsa(pkcs1pad, sha512),
  cbc, and ctr from crypto self-tests
- Added ECC pubkey generation and verification success messages
* Wed Nov 29 2023 Keerthana K <keerthanak@vmware.com> 6.1.56-6
- Modified ecdh-nist-p384 vector to generate ECC keypair
* Wed Nov 29 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-5
- Upgrade canister to 5.0.0-6.1.56-3
* Wed Nov 29 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-4
- Adding support for ACVP build
- Added jitterentropy implementation of SHA3-256
* Wed Nov 29 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-3
- Add missing self-test vector for ecdh-nist-p384 with genkey
* Wed Nov 29 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.56-2
- Jitterentropy wrapper changes.
* Wed Nov 29 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-1
- Upgrade to 6.1.56
* Wed Nov 29 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.53-6
- Fix for CVE-2023-42754
* Wed Nov 29 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-5
- Enable fips and update canister binary version 5.0.0-6.1.53-4
- Removed jent_lock struct from ignore list of check_fips_canister
* Wed Nov 29 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-4
- Add pkcs1pad test vectors in crytpo_self_test module
* Thu Nov 23 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-3
- Fix CVE-2023-42756
* Thu Nov 23 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-2
- Fix for CVE-2023-42755
* Thu Nov 23 2023 Roye Eshed <eshedr@vmware.com> 6.1.53-1
- Update to version 6.1.53
* Thu Nov 23 2023 Ajay Kaher <akaher@vmware.com> 6.1.45-7
- Fix: net: roundup issue in kmalloc_reserve()
* Thu Nov 23 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.45-6
- Move all prep to %prep section
* Thu Nov 23 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.45-5
- LKCM 5.0 specific changes to crypto self-tests and tcrypt
* Thu Nov 23 2023 Keerthana K <keerthanak@vmware.com> 6.1.45-4
- Build with jitterentropy v3.4.1
* Thu Nov 23 2023 Keerthana K <keerthanak@vmware.com> 6.1.45-3
- Update fips_canister version 6.1.45-3
* Wed Nov 22 2023 Ankit Jain <ankitja@vmware.com> 6.1.45-2
- Fix for CVE-2023-28464
* Wed Nov 22 2023 Ajay Kaher <akaher@vmware.com> 6.1.45-1
- Update to version 6.1.45
* Wed Nov 22 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.41-4
- Enable CONFIG_DEBUG_INFO_BTF=y
* Wed Nov 22 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.41-3
- Enable Kconfig CONFIG_KEXEC_FILE for kexec signature verify
* Wed Nov 22 2023 Ajay Kaher <akaher@vmware.com> 6.1.41-2
- Fix: unconditional preserve CR4.MCE
* Wed Nov 22 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.41-1
- Update to version 6.1.41
* Wed Nov 22 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.37-1
- Update to version 6.1.37
* Wed Nov 22 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.32-1
- Update to version 6.1.32
* Wed Nov 22 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.28-5
- disable kconfig CONFIG_RAID6_PQ_BENCHMARK
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.28-4
- Bump version as a part of openssl upgrade
* Tue Oct 03 2023 Kuntal Nayak <nkunal@vmware.com> 6.1.28-3
- Kconfig to lockdown kernel in UEFI Secure Boot
* Sat Sep 23 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.28-2
- Cherry pick performance over security option for RETBleed (pos=1)
- patch from Photon 4.0
* Wed Sep 20 2023 Ankit Jain <ankitja@vmware.com> 6.1.28-1
- Update to version 6.1.28
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-15
- Use canister version 5.0.0-6.1.37-2
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-14
- Bump version as a part of elfutils upgrade
* Fri Apr 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-13
- Remove dracut & initramfs from requires
* Wed Apr 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-12
- Remove rpi fan driver patch
* Wed Apr 05 2023 Ajay Kaher <akaher@vmware.com> 6.1.10-11
- perf: remove libunwind dependency
* Fri Mar 31 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.1.10-10
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Mar 30 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.10-9
- Update drivers
- iavf: 4.8.2
- ice: 1.11.14
- i40e: 2.22.18
* Sun Mar 26 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.10-8
- Use canister version 5.0.0-6.1.10-8
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-7
- Fix initramfs trigger
* Thu Mar 16 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-6
- Enable FIPS canister binary usage
* Tue Mar 07 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 6.1.10-5
- Add ENA and EFA drivers to ARM build
* Tue Mar 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-4
- Fix initrd driver list for aarch64
* Thu Mar 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-3
- Fix initrd generation logic
- Add dracut, initramfs to requires
* Fri Feb 24 2023 Ankit Jain <ankitja@vmware.com> 6.1.10-2
- Exclude iavf.conf
* Wed Feb 22 2023 Bo Gan <ganb@vmware.com> 6.1.10-1
- Update to 6.1.10
* Tue Feb 21 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-11
- Enable turbostat to work in the guest on VMware hypervisor.
* Tue Feb 21 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-10
- Update i40e driver to v2.19.3 to prevent kernel warnings
* Mon Feb 20 2023 Ajay Kaher <akaher@vmware.com> 6.0.7-9
- exclude man dir from linux-tools
* Thu Feb 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.0.7-8
- Fix requires
* Wed Jan 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.0.7-7
- Enable CONFIG_PCI_PF_STUB
* Tue Jan 17 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 6.0.7-6
- Depricate linux-aws kernel flavor
* Fri Jan 13 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-5
- Fix IRQ affinities of i40e, iavf and ice drivers
* Mon Jan 09 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-4
- Update Intel drivers i40e to v2.16.11, iavf to v4.5.3 and ice to v1.9.11
* Fri Jan 06 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-3
- Port patch to allow disabling PCI resets from vfio_pci driver to 6.0
- Move the module parameter disable_resets from vfio_pci to
- vfio_pci_core module, to make it work with kernel 6.0.
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.0.7-2
- Bump up due to change in elfutils
* Tue Dec 20 2022 Bo Gan <ganb@vmware.com> 6.0.7-1
- Update to 6.0.7
- Enable PREEMPT_DYNAMIC
- Enable extra Dell platform drivers.
- Enable security configs, RANDOMIZE_KSTACK_OFFSET and others.
- Change from SLAB to SLUB
- aarch64/config: match x86 on non-arch specific setting.
- aarch64/config: don't set CAVIUM_ERRATUM_23154 and wait for ESX support
* Mon Dec 19 2022 Dweep Advani <dadvani@vmware.com> 5.10.142-5
- Ignore warnings to keep building tools
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.10.142-4
- Dont throw error for supported deprecated modules of py311
* Thu Oct 20 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.142-3
- Fix build with latest toolchain
* Wed Sep 28 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-2
- Replace rpm macro 'name' with 'linux' to be consistent with other flavors.
* Wed Sep 28 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-1
- Update to version 5.10.142
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.132-1
- Update to version 5.10.132
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-10
- Backport fixes for CVE-2022-0500
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-9
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-8
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-7
- .config: enable CONFIG_NET_ACT_SIMP
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-6
- .config: enable CONFIG_X86_CPU_RESCTRL
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-5
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-4
- Avoid TSC recalibration
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-3
- Fix for CVE-2022-21505
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-2
- VMCI patches & configs
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-1
- Update to version 5.10.118
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.109-4
- Fix for CVE-2022-1966, CVE-2022-1972
* Thu Sep 22 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.109-3
- Fix for CVE-2022-21499
* Thu Sep 22 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.109-2
- Fix for CVE-2022-29582
* Wed Sep 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.109-1
- Update to version 5.10.109
* Tue Sep 20 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-4
- Fix for CVE-2022-1016
* Tue Sep 20 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-3
- Fix SEV and Hypercall alternative inst. patches
* Tue Sep 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.103-2
- Add bpftool subpackage
* Thu Sep 15 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-1
- Update to version 5.10.103
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-5
- Fix for CVE-2022-0435
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-4
- Fix for CVE-2022-0492
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-3
- Fix for CVE-2022-22942
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-2
- Fix CVE-2022-0330
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-1
- Update to version 5.10.93
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-5
- Fix CVE-2021-4155 and CVE-2021-4204
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-4
- Enable crypto related configs in aarch64 similar to x86_64
- crypto_self_test and broken kattest module enhancements
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-3
- mm: fix percpu allocation for memoryless nodes
- pvscsi: fix disk detection issue
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-2
- remove tmem, lvm in add-drivers list
- lvm drivers are built as part of dm-mod
- tmem module no longer exists
* Mon Sep 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-1
- Update to version 5.10.83
* Mon Sep 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-14
- .config: Enable eBPF net packet filtering support.
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-13
- Scriptlets fixes and improvements
* Wed Jul 20 2022 Tejaswini Jayaramaiah <jtejaswini@vmware.com> 5.10.78-12
- Enable CONFIG_CGROUP_BPF in config to run containers with cgroup v2
* Wed Jul 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-11
- Add PCI quirk to allow multiple devices under the same virtual
- PCI bridge to be put into separate IOMMU groups.
* Tue Jul 12 2022 Sharan Turlapati <sturlpati@vmware.com> 5.10.78-10
- Allow PCI resets to be disabled from vfio_pci
* Wed Jun 29 2022 Keerthana K <keerthanak@vmware.com> 5.10.78-9
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-8
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Tue Jun 14 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.78-7
- Enable CONFIG_LIVEPATCH, which requires enabling ftrace, and related.
* Tue Apr 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-6
- Enable CONFIG_EXT2_FS_XATTR & related parameters
* Tue Jan 25 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-5
- .config: enable squashfs module, enable crypto user api rng.
* Thu Nov 25 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-4
- Disable md5 algorithm for sctp if fips is enabled.
* Fri Nov 19 2021 Keerthana K <keerthanak@vmware.com> 5.10.78-3
- Add arm64 hypervisor detection and kmsg dumper
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.10.78-2
- compile with openssl 3.0.0
* Mon Nov 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.78-1
- Update to version 5.10.78
* Thu Oct 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.75-1
- Update to version 5.10.75
* Thu Sep 09 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.61-2
- .config enable CONFIG_MOUSE_PS2_VMMOUSE and CONFIG_INPUT_UINPUT
- Enable sta by default
* Fri Aug 27 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-1
- Update to version 5.10.61
* Wed Aug 18 2021 Keerthana K <keerthanak@vmware.com> 5.10.52-2
- Update ice driver to v1.6.4
- Update i40e driver to v2.15.9
- Update iavf driver to v4.2.7
* Fri Jul 23 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
- Update to version 5.10.52
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
- Fix for CVE-2021-33909
* Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
- Update to version 5.10.46
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- Remove XR usb driver support
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.35-4
- Fix for CVE-2021-3573
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-3
- Add Rpi fan driver
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-2
- Fix for CVE-2021-3564
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
- Fix for CVE-2021-23133
* Tue May 11 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
- .config: Enable MLX5_INFINIBAND
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-8
- Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
- CVE-2020-26145, CVE-2020-26141
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-7
- Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
* Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-6
- Remove buf_info from device accessible structures in vmxnet3
* Thu Apr 29 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.25-5
- Update canister binary.
- use jent by drbg and ecc.
- Enable hmac(sha224) self test and broket KAT test.
* Thu Apr 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.25-4
- Remove hmac(sha224) test from broken kat test.
* Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
- Fix for CVE-2021-23133
* Thu Apr 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.25-2
- Fix for CVE-2021-29154
* Mon Mar 22 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.25-1
- Update to version 5.10.25
* Sun Mar 21 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.21-3
- Do not execute some tests twice
- Support future disablement of des3
- Do verbose build
- Canister update.
* Mon Mar 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
- Use jitterentropy rng instead of urandom in rng module.
* Mon Mar 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-17
- FIPS canister update
* Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-16
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Fri Feb 19 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-15
- Added SEV-ES improvement patches
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-14
- Enable CONFIG_WDAT_WDT
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-13
- lower the loglevel for floppy driver
* Thu Feb 18 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-12
- Enable CONFIG_IFB
* Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-11
- Added latest out of tree version of Intel ice driver
* Tue Feb 16 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-10
- Fix perf compilation issue with gcc-10.2.0 for aarch64
* Mon Feb 15 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-9
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Wed Feb 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-8
- Update i40e driver to v2.13.10
- Add out of tree iavf driver
- Enable CONFIG_NET_TEAM
* Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-7
- Use secure FIPS canister.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-6
- Enabled CONFIG_WIREGUARD
* Fri Jan 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-5
- Build kernel with FIPS canister.
* Wed Jan 20 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-4
- Handle module.lds for aarch64 in the same way as for x86_64
* Wed Jan 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-3
- Remove traceevent/plugins from linux-tools
* Mon Jan 11 2021 Bo Gan <ganb@vmware.com> 5.10.4-2
- Fix aarch64 build failure
* Mon Jan 04 2021 Bo Gan <ganb@vmware.com> 5.10.4-1
- Update to 5.10.4
- Drop out-of-tree SEV-ES functional patches (already upstreamed).
* Wed Dec 09 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-9
- To dynamic load Overlays adding of_configfs patches v5.9.y.
* Tue Dec 01 2020 Prashant S Chauhan <psinghchauha@vmware.com> 5.9.0-8
- Added ami for arm support in linux generic, added multiple drivers
- in aarch64 to support aws ami
* Thu Nov 12 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-7
- .config: support for floppy disk and ch341 usb to serial
* Wed Nov 11 2020 Tapas Kundu <tkundu@vmware.com> 5.9.0-6
- Fix perf python script for compatibility with python 3.9
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-5
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-25704
* Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-3
- Remove the support of fipsify and hmacgen
* Tue Oct 27 2020 Piyush Gupta <gpiyush@vmware.com> 5.9.0-2
- Fix aarch64 build failure due to missing CONFIG_FB_ARMLCD
* Mon Oct 19 2020 Bo Gan <ganb@vmware.com> 5.9.0-1
- Update to 5.9.0
* Wed Sep 30 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
- Update to version 5.9.0-rc7
* Mon Sep 21 2020 Bo Gan <ganb@vmware.com> 5.9.0-rc4.1
- Update to 5.9.0-rc4
- AMD SEV-ES Support
- RPI4 Support
- config_common: Reduce linked-in modules
- Drop NXP LS10XXa board support
* Tue Sep 08 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-6
- Fix build failure with binutils updated to 2.35
* Wed Aug 05 2020 Sharan Turlapati <sturlapati@vmware.com> 4.19.127-5
- Enable CONFIG_TCP_CONG_BBR
* Wed Jul 29 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.127-4
- .config: add zram module
* Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
- Fix CVE-2020-14331
* Fri Jul 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-2
- Fix aarch64 build failure due to missing i40e man pages.
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Tue Jun 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.112-14
- Add latest out of tree version of i40e driver
* Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-13
- Enable CONFIG_VFIO_NOIOMMU
* Tue Jun 09 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-12
- Add intel_sgx module (-drivers-intel-sgx subpackage)
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.112-11
- Enabled CONFIG_BINFMT_MISC
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-10
- Add patch to fix CVE-2019-18885
* Mon Jun 1 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.112-9
- Keep modules of running kernel till next boot
* Sat May 30 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-8
- .config: add gs_usb module
* Wed May 20 2020 Tapas Kundu <tkundu@vmware.com> 4.19.112-7
- Added linux-python3-perf subpackage.
- Added turbostat and cpupower to tools for x86_64.
- linux-python3-perf replaces python3-perf.
* Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.112-6
- Add uio_pic_generic driver support in config
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-5
- Add patch to fix CVE-2020-10711
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-4
- Photon-checksum-generator version update to 1.1.
* Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-3
- Enable additional config options.
* Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-2
- HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
* Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
- Update to version 4.19.112
* Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
- hmac generation of crypto modules and initrd generation changes if fips=1
* Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
- Update to version 4.19.104
* Mon Mar 23 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.97-8
- Fix perf compilation issue with binutils >= 2.34.
* Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-7
- Adding Enhances depedency to hmacgen.
* Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-6
- Backporting of patch continuous testing of RNG from urandom
* Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-5
- Fix CVE-2019-16234
* Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-4
- Add photon-checksum-generator source tarball and remove hmacgen patch.
- Exclude hmacgen.ko from base package.
* Fri Jan 31 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-3
- Move snd-bcm2835.ko to linux-drivers-sound rpm
* Wed Jan 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-2
- Update tcrypt to test drbg_pr_sha256 and drbg_nopr_sha256.
- Update testmgr to add drbg_pr_ctr_aes256 test vectors.
* Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
- Update to version 4.19.97
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-6
- Enable DRBG HASH and DRBG CTR support.
* Wed Jan 08 2020 Ajay Kaher <akaher@vmware.com> 4.19.87-5
- Enabled configs RTC_DRV_PL030, RTC_DRV_PL031
* Fri Jan 03 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-4
- Modify tcrypt to remove tests for algorithms that are not supported in photon.
- Added tests for DH, DRBG algorithms.
* Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
- Update fips Kat tests patch.
* Mon Dec 09 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.87-2
- Cross compilation support
* Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
- Update to version 4.19.87
* Tue Dec 03 2019 Keerthana K <keerthanak@vmware.com> 4.19.84-4
- Adding hmac sha256/sha512 generator kernel module for fips.
* Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-3
- Fix CVE-2019-19062, CVE-2019-19066, CVE-2019-19072,
- CVE-2019-19073, CVE-2019-19074, CVE-2019-19078
* Mon Nov 18 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.84-2
- .config: infiniband support.
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
- Update to version 4.19.84
- Fix CVE-2019-18814
* Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Update to version 4.19.82
* Thu Nov 07 2019 Jorgen Hansen (VMware) <jhansen@vmware.com> 4.19.79-3
- Fix vsock QP detach with outgoing data
* Thu Oct 24 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-2
- Enabled WiFi and BT config for Dell 5K.
* Tue Oct 15 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
- Update to version 4.19.79
- Fix CVE-2019-17133
* Mon Oct 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-5
- Add megaraid_sas driver to initramfs
* Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-4
- Enable IMA with SHA256 as default hash algorithm
* Thu Oct 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.76-3
- Add additional BuildRequires and Requires to fix issues with perf, related to
- interactive UI and C++ symbol demangling. Also update the last few perf python
- scripts in Linux kernel to use python3 syntax.
* Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
- Adding lvm and dm-mod modules to support root as lvm
* Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
- Update to version 4.19.76
- Enable USB_SERIAL_PL2303 for aarch64
* Mon Sep 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
- Update to version 4.19.72
* Thu Sep 05 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-3
- Avoid oldconfig which leads to potential build hang
- Fix archdir usage
* Thu Sep 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.69-2
- Adding SPI and Audio interfaces in rpi3 device tree
- Adding spi0 and audio overlays
- Copying rpi dt in /boot/broadcom as u-boot picks from here
* Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
- Update to version 4.19.69
* Fri Aug 23 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-4
- NXP ls1046a frwy board support.
- config_aarch64: add fsl_dpaa2 support.
- fix fsl_dpaa_mac initialization issue.
* Wed Aug 14 2019 Raejoon Jung <rjung@vmware.com> 4.19.65-3
- Backport of Secure Boot UEFI certificate import from v5.2
* Mon Aug 12 2019 Ajay Kaher <akaher@vmware.com> 4.19.65-2
- Fix config_aarch64 for v4.19.65
* Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
- Update to version 4.19.65
- Fix CVE-2019-1125 (SWAPGS)
* Tue Jul 30 2019 Ajay Kaher <akaher@vmware.com> 4.19.52-7
- Added of_configfs patches to dynamic load Overlays.
* Thu Jul 25 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-6
- Fix postun scriplet.
* Thu Jul 11 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-5
- Enable kernel configs necessary for BPF Compiler Collection (BCC).
* Wed Jul 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-4
- Deprecate linux-aws-tools in favor of linux-tools.
* Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-3
- Fix 9p vsock 16bit port issue.
* Thu Jun 20 2019 Tapas Kundu <tkundu@vmware.com> 4.19.52-2
- Enabled CONFIG_I2C_CHARDEV to support lm-sensors
* Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
- Update to version 4.19.52
- Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
- CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
* Tue May 28 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
- Change default I/O scheduler to 'deadline' to fix performance issue.
* Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
- Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
- mulitple kernels are installed and current linux kernel is removed.
* Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
- Update to version 4.19.40
* Thu Apr 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-3
- Update config_aarch64 to fix ARM64 build.
* Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
- Fix CVE-2019-10125
* Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
- Update to version 4.19.32
* Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
- Update to version 4.19.29
* Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
- Update to version 4.19.26
* Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-3
- Fix CVE-2019-8912
* Thu Jan 24 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.15-2
- Add WiFi (ath10k), sensors (i2c,spi), usb support for NXP LS1012A board.
* Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
- Update to version 4.19.15
* Fri Jan 11 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-7
- Add Network support for NXP LS1012A board.
* Wed Jan 09 2019 Ankit Jain <ankitja@vmware.com> 4.19.6-6
- Enable following for x86_64 and aarch64:
-  Enable Kernel Address Space Layout Randomization.
-  Enable CONFIG_SECURITY_NETWORK_XFRM
* Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-5
- Enable AppArmor by default.
* Wed Jan 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
- .config: added Compulab fitlet2 device drivers
- .config_aarch64: added gpio sysfs support
- renamed -sound to -drivers-sound
* Tue Jan 01 2019 Ajay Kaher <akaher@vmware.com> 4.19.6-3
- .config: Enable CONFIG_PCI_HYPERV driver
* Wed Dec 19 2018 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-2
- Add NXP LS1012A support.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6
* Fri Dec 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
- .config: added qmi wwan module
* Mon Nov 12 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
- Fix config_aarch64 for 4.19.1
* Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
- Update to version 4.19.1
* Tue Oct 16 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.18.9-5
- Change in config to enable drivers for zigbee and GPS
* Fri Oct 12 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-4
- Enable LAN78xx for aarch64 rpi3
* Fri Oct 5 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-3
- Fix config_aarch64 for 4.18.9
- Add module.lds for aarch64
* Wed Oct 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-2
- Use updated steal time accounting patch.
- .config: Enable CONFIG_CPU_ISOLATION and a few networking options
- that got accidentally dropped in the last update.
* Mon Oct 1 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9
* Tue Sep 25 2018 Ajay Kaher <akaher@vmware.com> 4.14.67-2
- Build hang (at make oldconfig) fix in config_aarch64
* Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
- Update to version 4.14.67
* Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-7
- Add rdrand-based RNG driver to enhance kernel entropy.
* Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-6
- Add full retpoline support by building with retpoline-enabled gcc.
* Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-5
- Apply out-of-tree patches needed for AppArmor.
* Wed Aug 22 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-4
- Fix overflow kernel panic in rsi driver.
- .config: enable BT stack, enable GPIO sysfs.
- Add Exar USB serial driver.
* Fri Aug 17 2018 Ajay Kaher <akaher@vmware.com> 4.14.54-3
- Enabled USB PCI in config_aarch64
- Build hang (at make oldconfig) fix in config_aarch64
* Thu Jul 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-2
- .config: usb_serial_pl2303=m,wlan=y,can=m,gpio=y,pinctrl=y,iio=m
* Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
- Update to version 4.14.54
* Fri Jan 26 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-2
- Added vchiq entry to rpi3 dts
- Added dtb-rpi3 subpackage
* Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
- Version update
* Wed Dec 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-4
- KAT build support
* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-3
- Aarch64 support
* Tue Dec 05 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-2
- Sign and compress modules after stripping. fips=1 requires signed modules
* Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
- Version update
* Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
- Version update
* Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
- Version update
* Wed Oct 11 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-3
- Add patch "KVM: Don't accept obviously wrong gsi values via
    KVM_IRQFD" to fix CVE-2017-1000252.
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-2
- Build hang (at make oldconfig) fix.
* Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
- Version update
* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-3
- Allow privileged CLONE_NEWUSER from nested user namespaces.
* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-2
- Fix CVE-2017-11472 (ACPICA: Namespace: fix operand cache leak)
* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
- Version update
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-2
- Requires coreutils or toybox
* Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
- Fix CVE-2017-11600
* Tue Aug 22 2017 Anish Swaminathan <anishs@vmware.com> 4.9.43-2
- Add missing xen block drivers
* Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
- Version update
- [feature] new sysctl option unprivileged_userns_clone
* Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
- Fix CVE-2017-7542
- [bugfix] Added ccm,gcm,ghash,lzo crypto modules to avoid
    panic on modprobe tcrypt
* Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
- Version update
* Fri Aug 04 2017 Bo Gan <ganb@vmware.com> 4.9.38-6
- Fix initramfs triggers
* Tue Aug 01 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-5
- Allow some algorithms in FIPS mode
- Reverts 284a0f6e87b0721e1be8bca419893902d9cf577a and backports
- bcf741cb779283081db47853264cc94854e7ad83 in the kernel tree
- Enable additional NF features
* Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-4
- Add patches in Hyperv codebase
* Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-3
- Add missing hyperv drivers
* Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
- Disable scheduler beef up patch
* Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
- Fix CVE-2017-11176 and CVE-2017-10911
* Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-3
- Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 4.9.34-2
- Added obsolete for deprecated linux-dev package
* Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
- [feature] 9P FS security support
- [feature] DM Delay target support
- Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
* Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
- Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
- [feature] IPV6 netfilter NAT table support
* Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
- Added ENA driver for AMI
- Fix CVE-2017-7487 and CVE-2017-9059
* Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
- Enable IPVLAN module.
* Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
- Version update
* Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
- Version update
* Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
- Version update
- Removed version suffix from config file name
* Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
- Support dynamic initrd generation
* Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
- Fix CVE-2017-6874 and CVE-2017-7618.
- Fix audit-devel BuildRequires.
- .config: build nvme and nvme-core in kernel.
* Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
- .config: NSX requirements for crypto and netfilter
* Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
- Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
* Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
- Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
- .config: added CRYPTO_FIPS support.
* Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
- Update to linux-4.9.2 to fix CVE-2016-10088
- Move linux-tools.spec to linux.spec as -tools subpackage
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
- BuildRequires Linux-PAM-devel
* Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
- Update to linux-4.9.0
- Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
* Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
- net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
- Expand `uname -r` with release number
- Check for build-id matching
- Added syscalls tracing support
- Compress modules
* Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
- Update to linux-4.4.35
- vfio-pci-fix-integer-overflows-bitmask-check.patch
    to fix CVE-2016-9083
* Tue Nov 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-4
- net-9p-vsock.patch
* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-3
- tty-prevent-ldisc-drivers-from-re-using-stale-tty-fields.patch
    to fix CVE-2015-8964
* Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-2
- .config: add cgrup_hugetlb support
- .config: add netfilter_xt_{set,target_ct} support
- .config: add netfilter_xt_match_{cgroup,ipvs} support
* Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
- Update to linux-4.4.31
* Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
- Update to linux-4.4.26
* Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
- net-add-recursion-limit-to-GRO.patch
- scsi-arcmsr-buffer-overflow-in-arcmsr_iop_message_xfer.patch
* Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
- ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
- tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
* Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
- Package vmlinux with PROGBITS sections in -debuginfo subpackage
* Tue Sep 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
- .config: CONFIG_IP_SET_HASH_{IPMARK,MAC}=m
* Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
- Add -release number for /boot/* files
- Use initrd.img with version and release number
- Rename -dev subpackage to -devel
* Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
- Update to linux-4.4.20
- apparmor-fix-oops-validate-buffer-size-in-apparmor_setprocattr.patch
- keys-fix-asn.1-indefinite-length-object-parsing.patch
* Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
- vmxnet3 patches to bumpup a version to 1.4.8.0
* Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
- Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
- .config: pmem hotplug + ACPI NFIT support
- .config: enable EXPERT mode, disable UID16 syscalls
* Thu Jul 07 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
- .config: pmem + fs_dax support
* Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
- patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
- .config: disable rt group scheduling - not supported by systemd
* Wed Jun 15 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-7
- fixed the capitalization for - System.map
* Thu May 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
- patch: REVERT-sched-fair-Beef-up-wake_wide.patch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-5
- GA - Bump release of all rpms
* Mon May 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-4
- Fixed generation of debug symbols for kernel modules & vmlinux.
* Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-3
- Added patches to fix CVE-2016-3134, CVE-2016-3135
* Wed May 18 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-2
- Enabled CONFIG_UPROBES in config as needed by ktap
* Wed May 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
- Update to linux-4.4.8
- Added net-Drivers-Vmxnet3-set-... patch
* Tue May 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-27
- Compile Intel GigE and VMXNET3 as part of kernel.
* Thu Apr 28 2016 Nick Shi <nshi@vmware.com> 4.2.0-26
- Compile cramfs.ko to allow mounting cramfs image
* Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-25
- Revert network interface renaming disable in kernel.
* Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-24
- Support kmsg dumping to vmware.log on panic
- sunrpc: xs_bind uses ip_local_reserved_ports
* Mon Mar 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-23
- Enabled Regular stack protection in Linux kernel in config
* Thu Mar 17 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-22
- Restrict the permissions of the /boot/System.map-X file
* Fri Mar 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-21
- Patch: SUNRPC: Do not reuse srcport for TIME_WAIT socket.
* Wed Mar 02 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-20
- Patch: SUNRPC: Ensure that we wait for connections to complete
    before retrying
* Fri Feb 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
- Disable watchdog under VMware hypervisor.
* Thu Feb 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
- Added rpcsec_gss_krb5 and nfs_fscache
* Mon Feb 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-17
- Added sysctl param to control weighted_cpuload() behavior
* Thu Feb 18 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.0-16
- Disabling network renaming
* Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
- veth patch: don’t modify ip_summed
* Thu Feb 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-14
- Full tickless -> idle tickless + simple CPU time accounting
- SLUB -> SLAB
- Disable NUMA balancing
- Disable stack protector
- No build_forced no-CBs CPUs
- Disable Expert configuration mode
- Disable most of debug features from 'Kernel hacking'
* Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
- Double tcp_mem limits, patch is added.
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-12
- Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
* Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-11
- Revert CONFIG_HZ=250
* Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
- Fix for CVE-2016-0728
* Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
- CONFIG_HZ=250
* Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
- Remove rootfstype from the kernel parameter.
* Mon Jan 04 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-7
- Disabled all the tracing options in kernel config.
- Disabled preempt.
- Disabled sched autogroup.
* Thu Dec 17 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-6
- Enabled kprobe for systemtap & disabled dynamic function tracing in config
* Fri Dec 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-5
- Added oprofile kernel driver sub-package.
* Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-4
- Change the linux image directory.
* Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-3
- Added the build essential files in the dev sub-package.
* Mon Nov 09 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-2
- Enable Geneve module support for generic kernel.
* Fri Oct 23 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
- Upgraded the generic linux kernel to version 4.2.0 & and updated timer handling to full tickless mode.
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.9-5
- Added driver support for frame buffer devices and ACPI
* Wed Sep 2 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-4
- Added mouse ps/2 module.
* Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-3
- Use photon.cfg as a symlink.
* Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-2
- Added environment file(photon.cfg) for grub.
* Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
- Upgrading kernel version.
* Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19.2-5
- Updated OVT to version 10.0.0.
- Rename -gpu-drivers to -drivers-gpu in accordance to directory structure.
- Added -sound package/
* Tue Aug 11 2015 Anish Swaminathan<anishs@vmware.com> 3.19.2-4
- Removed Requires dependencies.
* Fri Jul 24 2015 Harish Udaiya Kumar <hudaiyakumar@gmail.com> 3.19.2-3
- Updated the config file to include graphics drivers.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.13.3-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
- Initial build. First version
