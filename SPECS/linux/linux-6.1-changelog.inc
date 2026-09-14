%changelog
* Mon Sep 14 2026 Daniel Casota <dcasota@gmail.com> 6.1.183-3
- Refuse acvp_build and kat_build on architectures other than x86_64
* Fri Sep 11 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.1.183-2
- Club linux-tools.spec into linux.spec
* Fri Aug 21 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.183-1
- Update to version 6.1.183
- Fix BPF JIT memory (bpf_jit_limit) leak from seccomp filters pinned by unreaped zombies
* Mon Aug 17 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.177-3
- Revert CVE-2026-53224, CVE-2026-53246 due to failing LTP
* Thu Jul 23 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.177-2
- Fixes CVE-2026-53224, CVE-2026-53246
* Tue Jul 14 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.177-1
- Update to version 6.1.177
* Fri Jul 10 2026 Ankit Jain <ankit-aj.ajin@broadcom.com> 6.1.176-4
- Pin UPAI enums: IFLA_BRPORT_SINK_CONNECTED=60, IFLA_GRE_MSS_CLAMP=30
- to make it consistent between 6.1/6.12 kernel and some headroom for future upgrades.
* Wed Jul 08 2026 Bo Gan <bo.gan@broadcom.com> 6.1.176-3
- Fix for vmxnet3 BUG_ON in vmxnet3_get_hdr_len()
* Tue Jun 30 2026 Harinadh Dommaraju <harinadh.dommaraju@broadcom.com> 6.1.176-2
- Fix CVE-2026-46266
* Wed Jun 24 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.176-1
- Update to version 6.1.176
* Tue Jun 23 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.175-11
- Fix CVE-2026-31675; add netem multi-segment skb corruption handling
* Sat Jun 20 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.1.175-10
- Add mpc-devel to build requires
* Fri Jun 12 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.175-9
- Fix CVE-2026-43456, CVE-2026-45850
* Fri Jun 12 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.175-8
- Fix CVE-2026-31505, CVE-2026-31502, CVE-2026-31557, CVE-2026-23383,
- CVE-2026-31419, CVE-2026-43083
* Fri Jun 12 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.175-7
- Fix CVE-2026-31709, CVE-2026-43249 and CVE-2026-23278
* Fri Jun 12 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.175-6
- Fix CVE-2026-43239, CVE-2026-43215, CVE-2026-43125
* Wed Jun 10 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.175-5
- Fix CVE-2026-31527, CVE-2026-31516
* Mon Jun 08 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.175-4
- Fix CVE-2026-23272, CVE-2026-23239
* Thu Jun 04 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.175-3
- Consolidate CVE patches into kernel_cve_patches.inc (range 3000-3999)
* Wed Jun 03 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.175-2
- Fix CVE-2026-43414
* Mon Jun 01 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.175-1
- Update to version 6.1.175
* Tue May 26 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.174-2
- Fix CVE-2026-23447, CVE-2026-31613, CVE-2026-31648, CVE-2026-31663
* Mon May 25 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.1.174-1
- Update to version 6.1.174
* Tue May 19 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.1.172-3
- Fix build with glibc-2.43
- Move linux-tools out to a different spec
* Fri May 15 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.172-2
- Fix CVE-2026-31685
* Mon May 11 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.172-1
- Update to version 6.1.172
* Mon May 04 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.1.170-1
- Update to version 6.1.170
* Wed Apr 22 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.169-1
- Update to version 6.1.169
* Tue Apr 14 2026 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.167-3
- Fix CVE-2026-23442, CVE-2026-23444
* Mon Apr 13 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.167-2
- Fix CVE-2026-23171
* Tue Apr 07 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.167-1
- Update to version 6.1.167
- Drop usb-acm-exclude-exar-usb-serial-ports-nxt.patch,
- cdc-acm will handle the device as a fallback
- Drop CVE-2025-40135, CVE-2025-38201, CVE-2025-38704, CVE-2023-53510,
- CVE-2026-23277: addressed in upstream 6.1.167
* Sat Apr 04 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.1.166-3
- Security fixes: CVE-2026-23407, CVE-2026-23408, CVE-2026-23410
- CVE-2026-23411
* Mon Mar 23 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.166-2
- Fix CVE-2026-23268, CVE-2026-23277
* Tue Mar 10 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.166-1
- Update to version 6.1.166
* Sat Mar 07 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.1.164-2
- Move aarch64 CVE fix patches out of aarch64 guard
* Tue Feb 24 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.164-1
- Update to version 6.1.164
* Wed Feb 18 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.163-2
- Fix CVE-2025-71184
* Tue Feb 17 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.163-1
- Update to version 6.1.163
* Sat Feb 07 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.161-8
- Fixes CVE-2025-68190, CVE-2024-25742 and CVE-2024-25743
* Fri Feb 06 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.161-7
- Fix for CVE-2023-54271 and CVE-2026-22999
* Fri Feb 06 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.161-6
- Fix CVE-2025-68353
* Tue Feb 03 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.161-5
- modpost: restore "undefined symbols" warning/errors back
* Fri Jan 30 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.161-4
- Fix for CVE-2023-53510
* Fri Jan 30 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.1.161-3
- Security fixes: CVE-2026-23001, CVE-2026-23010, CVE-2026-23011
* Sun Jan 25 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.1.161-2
- CVE-2025-71068
* Tue Jan 20 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.161-1
- Update to version 6.1.161
* Tue Jan 20 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.160-3
- Fixes CVE-2025-38718
* Mon Jan 19 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.160-2
- Fixes CVE-2025-68219 and CVE-2025-40328
* Tue Jan 13 2026 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.160-1
- Update to version 6.1.160
* Fri Jan 09 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.159-10
- Fix CVE-2025-68379, CVE-2025-68372
* Fri Jan 02 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.159-9
- Fixes CVE-2025-68188
* Wed Dec 31 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.159-8
- Fix CVE-2025-68724
* Mon Dec 29 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.159-7
- Fix CVE-2024-53095
* Tue Dec 23 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.159-6
- Fixes CVE-2025-39905
* Tue Dec 23 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.159-5
- Fixes CVE-2025-40362
* Wed Dec 17 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.159-4
- CVE-2024-53177
* Mon Dec 15 2025 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.159-3
- Fix CVE-2025-40135
* Wed Dec 10 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.159-2
- Fix SBAT validation order
* Mon Dec 08 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.159-1
- Update to version 6.1.159
* Sun Dec 07 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.158-13
- Fix CVE-2025-38248, CVE-2025-38584, CVE-2025-38616, CVE-2025-39797
- Fix CVE-2025-39810
* Tue Dec 02 2025 Bo Gan <bo.gan@broadcom.com> 6.1.158-12
- Fix CVE-2025-38129
* Mon Dec 01 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.158-11
- Fixes CVE-2025-39744
* Mon Dec 01 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.158-10
- Regression fix for CVE-2024-38557 fix
* Fri Nov 28 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.158-9
- Fixes CVE-2025-38704
* Wed Nov 26 2025 Mukul Sikka <mukul.sikka@broadcom.com> 6.1.158-8
- Fix CVE-2025-38081, CVE-2025-38201, CVE-2025-38361, CVE-2025-38636
* Wed Nov 26 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.158-7
- Fix CVE-2025-2312
* Wed Nov 26 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.158-6
- Fixes CVE-2025-37750, CVE-2025-40149 and CVE-2025-38556
* Tue Nov 18 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.158-5
- Fix CVE-2025-40110
* Mon Nov 17 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.158-4
- Fix newidle balance regression
* Thu Nov 13 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.158-3
- Fix CVE-2025-39990
* Wed Nov 12 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.158-2
- Fix CVE-2025-22121
* Tue Nov 11 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.158-1
- Update to version 6.1.158
* Fri Nov 07 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.157-5
- Fix CVE-2025-22022
* Thu Oct 30 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.157-4
- Fix CVE-2025-38057, CVE-2025-38073, CVE-2025-38039,
- CVE-2025-38045, CVE-2025-38064, CVE-2025-38022
* Thu Oct 30 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.157-3
- Fixes CVE-2024-49968, CVE-2024-49922 and CVE-2024-49988.
* Wed Oct 22 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.157-2
- Fix CVE-2025-39901 in aarch64, CVE-2024-41045
* Mon Oct 20 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.157-1
- Update to version 6.1.157
* Mon Oct 20 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.155-6
- Inject photon KM certificate to trusted keyring
* Mon Oct 13 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.155-5
- Fix CVE-2024-35949
* Mon Oct 13 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.155-4
- Fixes CVE-2025-38705 and CVE-2025-39705
* Mon Oct 13 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.155-3
- Fix CVE-2024-57795
* Mon Oct 13 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.155-2
- Fix CVE-2023-52653, CVE-2024-26661, CVE-2024-26662, CVE-2024-26944
* Fri Oct 10 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.155-1
- Update to version 6.1.155
* Tue Oct 07 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.153-3
- Disable building of DRM nouveau driver
* Mon Sep 29 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.153-2
- Fix CVE-2024-38564
* Wed Sep 24 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.153-1
- Update to version 6.1.153
* Mon Sep 22 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.148-3
- Fix CVE-2024-56611
* Wed Sep 03 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.148-2
- .config: enable CONFIG_NF_FLOW_TABLE=m
* Mon Aug 25 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.148-1
- Update to version 6.1.148
- Disable canister_build
* Fri Aug 22 2025 Bo Gan <bo.gan@broadcom.com> 6.1.147-7
- Fix regression introduced by CVE-2025-38465 fix
* Thu Aug 21 2025 Mounesh Badiger <mounesh.badiger@broadcom.com> 6.1.147-6
- linux:Add viomem kernel module
* Tue Aug 19 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.147-5
- Fix CVE-2024-57982
* Sat Aug 16 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.147-4
- Fix requires on doc sub package
* Tue Aug 12 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.147-3
- Override false positive network copyleft license detections
* Mon Aug 04 2025 Jonathan Shao <jonathan.shao@broadcom.com> 6.1.147-2
- Fix a kernel crash happened in get_rps_cpu() introduced by the HCX rps flow balance patch
* Mon Jul 28 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.147-1
- Update to version 6.1.147
* Fri Jul 18 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.143-3
- fix aarch64 build
* Mon Jul 14 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.143-2
- fix for vmxnet3
* Mon Jul 07 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.143-1
- Update to version 6.1.143
* Mon Jun 30 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.141-7
- Fix CVE-2024-27042, CVE-2024-26669
* Fri Jun 27 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.141-6
- Disable Bluetooth and CAN support
* Thu Jun 26 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.141-5
- Fix CVE-2025-21969
* Mon Jun 23 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.141-4
- Report guest crash to vmware hypervisor
* Mon Jun 23 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.141-3
- Fix CVE-2024-53068, CVE-2024-53168, CVE-2024-53179
* Wed Jun 18 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.141-2
- Fix CVE-2024-46813
* Mon Jun 09 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.141-1
- Update to version 6.1.141
* Fri May 16 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.138-2
- Introduce /sys/kernel/vmgenid
* Sun May 11 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.138-1
- Update to version 6.1.138
* Sun Apr 27 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.135-1
- Update to version 6.1.135
* Mon Apr 14 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.133-1
- Update to version 6.1.133
- Fixes: CVE-2025-21714, CVE-2025-21739 and CVE-2025-21759
* Mon Apr 14 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.131-3
- Fix recognition of cmdline param 'pti'/'nopti'
* Tue Apr 08 2025 Jonathan Shao <jonathan.shao@broadcom.com> 6.1.131-2
- Port xfrm policy cache mechanism from 4.14 kernel
* Fri Mar 28 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.131-1
- Update to version 6.1.131
* Mon Mar 24 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.130-4
- Fix CVE-2025-21863
* Thu Mar 20 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.130-3
- Bump-up to build with kmod-34.1
* Mon Mar 10 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.130-2
- Enable CONFIG_NFT_FIB_IPV4 and CONFIG_NFT_FIB_IPV6
* Wed Mar 05 2025 Harinadh Dommaraju <harinadh.dommaraju@broadcom.com> 6.1.130-1
- Update to version 6.1.130
* Tue Feb 18 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.128-2
- HCX patchset: fix deadlock while reading /proc/net/softnet_stat
* Mon Feb 03 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.128-1
- Update to version 6.1.128
* Fri Jan 24 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.126-5
- Fixes CVE-2024-56729, CVE-2024-38557
- CVE-2024-56647 and CVE-2024-56703
* Fri Jan 24 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.126-4
- Fixes CVE-2024-56631
* Fri Jan 24 2025 Srinidhi Rao <srnidhi.rao@broadcom.com> 6.1.126-3
- Increase max_jent_insts of jent_proxy to 32
* Thu Jan 23 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.126-2
- Add network required option for PE image signing
* Tue Jan 21 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.126-1
- Update to version 6.1.126
* Wed Jan 15 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.124-1
- Update to version 6.1.124
* Mon Jan 13 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.118-13
- Sign PE image inplace with SRP signer
* Mon Dec 30 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.118-12
- Improve fips canister struct definition check
* Mon Dec 23 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.118-11
- Fix build error in acvp build and some spec refinement
* Fri Dec 20 2024 Mukul Sikka <mukul.sikka@broadcom.com> 6.1.118-10
- Fix license for aarch64
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.118-9
- Release bump for SRP compliance
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.1.118-8
- Fix UDF directory traversal regression
* Mon Dec 09 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.118-7
- Disable CONFIG_GCC_PLUGIN_LATENT_ENTROPY
* Fri Dec 06 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.118-6
- fix aarch64 build
* Tue Nov 26 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.118-5
- Fix CVE-2024-50055, Fix CVE-2024-50014, CVE-2024-50018
* Tue Nov 26 2024 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.118-4
- Disable unique naming for *.ko.debug to make crash utility happy
* Tue Nov 26 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.118-3
- Disabled DYNAMIC_PREEMPT config
- rcutree: added new rcutree param to control max batch limit for cb
* Fri Nov 22 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.118-2
- sev-snp: fix vmwgfx crash
* Tue Nov 19 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.118-1
- Update to version 6.1.118
* Mon Nov 18 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.114-6
- New addition of jitterentropy RNG proxy.
* Mon Nov 18 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.114-5
- Fix CVE-2024-46816
* Thu Nov 14 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.114-4
- Fix strcture aead_geniv_ctx incompatibility between canister and vmlinux
* Tue Nov 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.114-3
- sev-snp: fix boot issue by parsing MP tables
* Thu Nov 07 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.114-2
- CVE-2024-50029, CVE-2024-50047
* Tue Nov 05 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.114-1
- Update to version 6.1.114
* Mon Oct 21 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.112-2
- Fix CVE-2024-41013, CVE-2024-41014
* Fri Oct 18 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.112-1
- Update to version 6.1.112
- Fix CVE-2024-46809, CVE-2024-46811, CVE-2024-46841, CVE-2024-46834, CVE-2024-46786
* Tue Oct 08 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.111-3
- Fix CVE-2024-42322
* Thu Oct 03 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.111-2
- In jitterentropy, use vzalloc instead of kzalloc.
* Fri Sep 20 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.111-1
- Update to version 6.1.111
* Wed Sep 11 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.109-2
- Fix CVE-2024-24855
* Tue Sep 10 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.109-1
- Update to version 6.1.109
* Tue Sep 10 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.106-8
- Fix CVE-2024-42228
* Sat Sep 07 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.106-7
- Fix CVE-2024-41071
* Wed Sep 04 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.106-6
- Fix CVE-2024-43859, CVE-2024-43835
* Wed Sep 04 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.106-5
- Enable CONFIG_NFT_OBJREF, so that we can refer counter by name
* Tue Sep 03 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.106-4
- Enable CONFIG_ARM64_ERRATUM_3194386
* Thu Aug 29 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.106-3
- HCX: Fix arp_probe_src_mac sysfs entry issue
- HCX: Fix rps_cpus to honor isolcpus range
* Tue Aug 27 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.106-2
- Fix CVE-2024-42314
* Tue Aug 20 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.106-1
- Update to version 6.1.106
* Tue Aug 20 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.102-3
- Binary patch aesni_cpu_id value in canister
* Wed Aug 14 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.102-2
- Enable CONFIG_GVE for gVNIC support
* Thu Aug 08 2024 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.102-1
- Upgrade to version 6.1.102
* Tue Aug 06 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.97-4
- Fix hcx crash while executing rmmod ipip
* Fri Jul 19 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.97-3
- Keep .BTF section in kernel modules
* Fri Jul 19 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.97-2
- Multiple HCX patch fixes.
* Wed Jul 10 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.97-1
- Update to version 6.1.97
* Thu Jun 27 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.94-2
- Ported HCX kernel patches and config changes
* Wed Jun 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 6.1.94-1
- Update to version 6.1.94
* Mon May 20 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.90-5
- perf: add patch to collect off-cpu sample
* Mon May 20 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.90-4
- Optimize gdb commands in check_fips_canister_compatibility script
* Fri May 17 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.90-3
- linux-generic will now obsolete and provide linux-secure as linux-secure
  has been merged into linux-generic. This will ensure tdnf update on
  Photon 5.0 is handled gracefully.
* Fri May 17 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.90-2
- Re-enable CONFIG_SECURITY_SELINUX_DEVELOP to fix boot time regressions
  in stig hardened systems.
* Mon May 13 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.90-1
- Update to version 6.1.90
- Fix aarch64 builds
* Thu May 02 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.83-5
- Port secure kernel changes to generic
* Tue Apr 23 2024 Roye Eshed <roye.eshed@broadcom.com> 6.1.83-4
- Fix for CVE-2023-52586 by disabling CONFIG_DRM_MSM
* Thu Apr 18 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.83-3
- Enable CONFIG_ATA_PIIX for ata/pata intel SFF drivers replacing legacy IDE drivers
* Sun Apr 14 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.83-2
- Patched CVE-2024-26643
* Thu Apr 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.83-1
- Update to version 6.1.83
- Fix CVE-2024-26642
* Mon Apr 8 2024  Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.81-5
- Update SBAT verification
* Wed Mar 27 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.81-4
- Fix CVE-2024-52452
* Wed Mar 27 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.81-3
- Fix CVE-2023-52585
* Mon Mar 25 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.81-2
- Patched CVE-2024-26585
* Wed Mar 06 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 6.1.81-1
- Update to version 6.1.81, patched CVE-2024-26584
* Wed Mar 06 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.79-2
- Fixes CVE-2024-23307 and CVE-2024-22099
* Mon Feb 26 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.79-1
- Update to version 6.1.79
* Tue Feb 13 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.77-1
- Update to version 6.1.77
* Tue Feb 06 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.75-3
- Update canister version to 5.0.0-6.1.75-2
* Wed Jan 31 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.75-2
- Upgrade iavf to v4.9.5 and ice to 1.13.7
* Wed Jan 31 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.75-1
- Update to version 6.1.75
* Wed Jan 31 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.70-5
- Enable CONFIG_PROC_EVENTS
* Tue Jan 23 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.70-4
- Fix CVE-2023-6915
* Wed Jan 17 2024 Bryan Tan <bryan-bt.tan@broadcom.com> 6.1.70-3
- Fix refcount underflow in vsock
* Tue Jan 16 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.70-2
- Fix CVE-2024-0340
* Mon Jan 01 2024 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.70-1
- Update to version 6.1.70
* Thu Dec 14 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.62-11
- print kernel crypto API return status for LKCM5 demo
- move all the ACVP related patches under a dedicated directory called
  acvp_patches
* Thu Dec 14 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-10
- Update canister to 5.0.0-6.1.62-13
* Thu Dec 14 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-9
- FIPS: Add log messages for approved and non-approved services
- Remove fips=2 logic
* Tue Dec 12 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.62-8
- Fix CVE-2023-39191
* Fri Dec 08 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.62-7
- Added self-tests for rsa-pkcs1pad in combination with sha1, sha224, sha384 and sha512
* Mon Nov 27 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.62-6
- Fix CVE-2023-5633
* Sat Nov 25 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-5
- Update canister to 5.0.0-6.1.62-7
* Wed Nov 22 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.62-4
- Fix for CVE-2023-2176
* Tue Nov 21 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-3
- Update canister to 5.0.0-6.1.62-2
* Sat Nov 18 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-2
- Fix RSA self tests
* Tue Nov 14 2023 Ankit Jain <ankitja@vmware.com> 6.1.62-1
- Update to version 6.1.62
* Fri Oct 27 2023 Ankit Jain <ankitja@vmware.com> 6.1.60-4
- Fix for CVE-2023-0597
* Fri Oct 27 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.60-3
- Remove kat_build and its associated spec changes
* Fri Oct 27 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.60-2
- Jitterentropy sample collection support in ACVP Build.
* Fri Oct 27 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.60-1
- Upgrade to 6.1.60
* Thu Oct 26 2023 Alexey Makhalov <amakhalov@vmware.com> 6.1.56-9
- Add .sbat section for bzImage
- Introduce SBAT verificaion in addition to signature on kexec
* Thu Oct 26 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-8
- Upgrade canister to 5.0.0-6.1.56-6
* Tue Oct 24 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-7
- Added cts to crypto self-tests
- Removed rsa(pkcs1pad, sha256), rsa(pkcs1pad, sha512),
  cbc, and ctr from crypto self-tests
- Added ECC pubkey generation and verification success messages
* Wed Oct 18 2023 Keerthana K <keerthanak@vmware.com> 6.1.56-6
- Modified ecdh-nist-p384 vector to generate ECC keypair
* Tue Oct 17 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-5
- Upgrade canister to 5.0.0-6.1.56-3
* Fri Oct 13 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-4
- Adding support for ACVP build
- Added jitterentropy implementation of SHA3-256
* Tue Oct 10 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-3
- Add missing self-test vector for ecdh-nist-p384 with genkey
* Mon Oct 09 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.56-2
- Jitterentropy wrapper changes.
* Fri Oct 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-1
- Upgrade to 6.1.56
* Tue Oct 03 2023 Kuntal Nayak <nkunal@vmware.com> 6.1.53-7
- Kconfig to lockdown kernel in UEFI Secure Boot
* Sun Oct 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.53-6
- Fix for CVE-2023-42754
* Fri Sep 29 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-5
- Enable fips and update canister binary version 5.0.0-6.1.53-4
- Removed jent_lock struct from ignore list of check_fips_canister
* Tue Sep 26 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-4
- Add pkcs1pad test vectors in crytpo_self_test module
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-3
- Fix CVE-2023-42756
* Mon Sep 25 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-2
- Fix for CVE-2023-42755
* Mon Sep 18 2023 Roye Eshed <eshedr@vmware.com> 6.1.53-1
- Update to version 6.1.53
* Fri Sep 15 2023 Ajay Kaher <akaher@vmware.com> 6.1.45-8
- Fix: net: roundup issue in kmalloc_reserve()
* Mon Sep 11 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.45-7
- Move all prep to %prep section
* Mon Sep 11 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.45-6
- LKCM 5.0 specific changes to crypto self-tests and tcrypt
* Fri Sep 08 2023 Keerthana K <keerthanak@vmware.com> 6.1.45-5
- Build with jitterentropy v3.4.1
* Fri Sep 08 2023 Keerthana K <keerthanak@vmware.com> 6.1.45-4
- Update fips_canister version 6.1.45-4
* Tue Sep 05 2023 Ankit Jain <ankitja@vmware.com> 6.1.45-3
- Fix for CVE-2023-28464
* Sat Sep 02 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.45-2
- Cherry pick performance over security option for RETBleed (pos=1)
- patch from Photon 4.0
* Mon Aug 14 2023 Ajay Kaher <akaher@vmware.com> 6.1.45-1
- Update to version 6.1.45
* Wed Aug 09 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.41-4
- Enable CONFIG_DEBUG_INFO_BTF=y
* Wed Aug 02 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.41-3
- Enable Kconfig CONFIG_KEXEC_FILE for kexec signature verify
* Mon Jul 31 2023 Ajay Kaher <akaher@vmware.com> 6.1.41-2
- Fix: unconditional preserve CR4.MCE
* Thu Jul 20 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.41-1
- Update to version 6.1.41
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 6.1.37-2
- Use canister version 5.0.0-6.1.37-2
* Tue Jul 04 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.37-1
- Update to version 6.1.37
* Tue Jun 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.32-1
- Update to version 6.1.32
* Tue May 23 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.28-2
- disable kconfig CONFIG_RAID6_PQ_BENCHMARK
* Tue May 16 2023 Ankit Jain <ankitja@vmware.com> 6.1.28-1
- Update to version 6.1.28
* Fri May 12 2023 Ajay Kaher <akaher@vmware.com> 6.1.10-13
- perf: remove libunwind dependency
- Remove rpi fan driver patch
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-12
- Remove dracut & initramfs from requires
* Thu Apr 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.10-11
- Use canister version 5.0.0-6.1.10-10
* Thu Apr 06 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.1.10-10
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Mar 30 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.10-9
- Update drivers
- iavf: 4.8.2
- ice: 1.11.14
- i40e: 2.22.18
* Fri Mar 24 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-8
- Disable FIPS canister binary usage
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
