%changelog
* Fri Aug 21 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.183-1
- Update to version 6.1.183
- Fix BPF JIT memory (bpf_jit_limit) leak from seccomp filters pinned by unreaped zombies
* Thu Aug 20 2026 Garrett Goble <Garrett.Goble@broadcom.com> 6.1.177-4
- Update SBX driver
* Mon Aug 17 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.177-3
- Revert fix for CVE-2026-53224, CVE-2026-53246 due to failing LTP
* Thu Jul 23 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.177-2
- Fixes CVE-2026-53224, CVE-2026-53246
* Tue Jul 14 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.177-1
- Update to version 6.1.177
* Wed Jul 08 2026 Bo Gan <bo.gan@broadcom.com> 6.1.176-3
- Fix for vmxnet3 BUG_ON in vmxnet3_get_hdr_len()
* Tue Jun 30 2026 Harinadh Dommaraju <harinadh.dommaraju@broadcom.com> 6.1.176-2
- Fix CVE-2026-46266
* Wed Jun 24 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.176-1
- Update to version 6.1.176
* Tue Jun 23 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.175-12
- Fix CVE-2026-31675; add netem multi-segment skb corruption handling
* Sat Jun 20 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.1.175-11
- Add mpc-devel to build requires
* Thu Jun 18 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.175-10
- Fix CVE-2026-43456, CVE-2026-45850
* Wed Jun 17 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.175-9
- Fix CVE-2026-31505, CVE-2026-31502, CVE-2026-31557, CVE-2026-23383
- CVE-2026-31419, CVE-2026-43083
* Tue Jun 16 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.175-8
- NEWCA initrd: fix hardlink sealing
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
- Fix CVE-2026-23447, CVE-2026-31613, CVE-2026-31663, CVE-2026-31648
* Mon May 25 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.1.174-1
- Update to version 6.1.174
* Fri May 22 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.172-4
- Removed xerces-c-devel from BuildRequires
* Fri May 15 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.172-3
- Fix CVE-2026-31685
* Wed May 13 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.172-2
- Remove libdnet BuildReuires dependency.
* Mon May 11 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.172-1
- Update to version 6.1.172
* Mon May 04 2026 Gerrit Photon <svc.photon-ci@broadcom.com> 6.1.170-1
- Update to version 6.1.170
* Wed Apr 29 2026 Mounesh Badiger <mounesh.badiger@broadcom.com> 6.1.169-2
- viomem: Add IOCTL to re-size the viomem memory
* Wed Apr 22 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.169-1
- Update to version 6.1.169
* Tue Apr 14 2026 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.167-3
- Fix CVE-2026-23442, CVE-2026-23444
* Mon Apr 13 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.167-2
- Fix CVE-2026-23171
* Tue Apr 07 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.167-1
- Update to version 6.1.167
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
* Sat Feb 07 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.161-7
- Fixes CVE-2025-68190, CVE-2024-25742 and CVE-2024-25743
* Fri Feb 06 2026 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.161-6
- Fix for CVE-2023-54271 and CVE-2026-22999
* Fri Jan 30 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.161-5
- Fix CVE-2025-68353
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
* Fri Jan 09 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.159-7
- Fix CVE-2025-68379, CVE-2025-68372
* Fri Jan 02 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.159-6
- Fixes CVE-2025-68188
* Wed Dec 31 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.159-5
- Fix CVE-2025-68724
* Mon Dec 29 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.159-4
- Fix CVE-2024-53095
* Wed Dec 10 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.159-3
- CVE-2024-53177
* Tue Dec 09 2025 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.159-2
- Fix CVE-2025-40135
* Mon Dec 08 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.159-1
- Update to version 6.1.159
* Sun Dec 07 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.158-14
- Fix CVE-2025-38248, CVE-2025-38584, CVE-2025-38616, CVE-2025-39797
* Fri Dec 05 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.158-13
- .config: enable mlx5 infiniband (=m) for Driver VM
* Tue Dec 02 2025 Bo Gan <bo.gan@broadcom.com> 6.1.158-12
- Fix CVE-2025-38129
* Mon Dec 01 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.158-11
- Fixes CVE-2025-39744
* Mon Dec 01 2025 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.158-10
- .config: enable mlx5 device driver (=m) for Driver VM
- Regression fix for CVE-2024-38557 fix
- .config: disable questionable ethernet devices support (cleanup)
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
* Mon Nov 10 2025 Junlong Gao <junlong.gao@broadcom.com> 6.1.157-6
- linux:Enable viomem kernel module for aarch64 build
* Fri Nov 07 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.157-5
- Fix CVE-2025-22022
* Thu Oct 30 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.157-4
- Fix CVE-2025-38057, CVE-2025-38073, CVE-2025-38039,
- CVE-2025-38045, CVE-2025-38064, CVE-2025-38022
* Thu Oct 30 2025 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.157-3
- Fixes CVE-2024-49968, CVE-2024-49922 and CVE-2024-49988.
* Wed Oct 22 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.157-2
- Fix CVE-2024-41045
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
* Mon Sep 29 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.153-3
- Fix CVE-2024-38564
* Fri Sep 26 2025 Mounesh Badiger <mounesh.badiger@broadcom.com> 6.1.153-2
- linux:Add viomem kernel module
* Wed Sep 24 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.153-1
- Update to version 6.1.153
* Mon Sep 22 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.148-2
- Fix CVE-2024-56611
* Mon Aug 25 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.148-1
- Update to version 6.1.148
* Wed Aug 20 2025 Bo Gan <bo.gan@broadcom.com> 6.1.147-4
- Fix regression introduced by CVE-2025-38465 fix
* Tue Aug 19 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.147-3
- Fix CVE-2024-57982
* Tue Aug 12 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.147-2
- Override false positive network copyleft license detections
* Mon Jul 28 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.147-1
- Update to version 6.1.147
* Fri Jul 18 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.143-3
- fix aarch64 build
* Mon Jul 14 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.143-2
- fix for vmxnet3
* Mon Jul 07 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.143-1
- Update to version 6.1.143
* Mon Jun 30 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.141-6
- Fix CVE-2024-27042, CVE-2024-26669
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
* Thu May 22 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.138-2
- Enable CONFIG_MTD, CONFIG_PCIE_PTM
* Sun May 11 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.138-1
- Update to version 6.1.138
* Sun Apr 27 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.135-1
- Update to version 6.1.135
* Tue Apr 22 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.133-1
- Update to version 6.1.133
- Fixes: CVE-2025-21714, CVE-2025-21739 and CVE-2025-21759
* Fri Apr 18 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.131-3
- Fix tarfs for inode count and -EBUSY issue
* Fri Apr 04 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.131-2
- Fix recognition of kcmdline param 'pti'/'nopti'
* Fri Mar 28 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.131-1
- Update to version 6.1.131
* Mon Mar 24 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.130-3
- Fix CVE-2025-21863
* Thu Mar 20 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.130-2
- Bump-up to build with kmod-34.1
* Wed Mar 05 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.130-1
- Update to version 6.1.130
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
- Add network required option with PE image signing
* Tue Jan 21 2025 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.126-1
- Update to version 6.1.126
* Wed Jan 15 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.124-1
- Update to version 6.1.124
* Mon Jan 13 2025 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.118-11
- Sign PE image inplace with SRP signer
* Mon Jan 13 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.118-10
- Fix aarch64 build
* Mon Dec 30 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.118-9
- Improve fips canister struct definition check
* Tue Dec 17 2024 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.118-8
- newca: fix panic when sealing hardlinks.
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.118-7
- Release bump for SRP compliance
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.1.118-6
- Fix UDF directory traversal regression
* Fri Dec 06 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.118-5
- fix aarch64 build
* Tue Nov 26 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.118-4
- Fix CVE-2024-50055, Fix CVE-2024-50014, CVE-2024-50018
* Tue Nov 26 2024 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.118-3
- Disable unique naming for *.ko.debug to make crash utility happy
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
* Mon Oct 28 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.112-3
- Fix CVE-2024-41013, CVE-2024-41014
* Fri Oct 25 2024 Alexey Makhalov <alexey.makhalov@broadcom.com> 6.1.112-2
- newca: avoid modifications of initrd pages.
* Fri Oct 18 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.112-1
- Update to version 6.1.112
- Fix CVE-2024-46809, CVE-2024-46811, CVE-2024-46841, CVE-2024-46834, CVE-2024-46786
* Tue Oct 08 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.111-3
- Fix CVE-2024-42322
* Thu Oct 03 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.111-2
- In jitterentropy, use vzalloc instead of kzalloc.
* Fri Sep 20 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.111-1
- Update to version 6.1.111
* Tue Sep 10 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.109-1
- Update to version 6.1.109
* Tue Sep 10 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.106-6
- Fix CVE-2024-42228
* Wed Sep 04 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 6.1.106-5
- Fix CVE-2024-43859, CVE-2024-43835
* Wed Sep 04 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.106-4
- Enable CONFIG_NFT_OBJREF, so that we can refer counter by name
* Tue Sep 03 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.106-3
- Enable CONFIG_ARM64_ERRATUM_3194386
* Tue Aug 27 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.106-2
- Fix CVE-2024-42314
* Tue Aug 20 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.106-1
- Update to version 6.1.106
* Tue Aug 20 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.102-2
- Binary patch aesni_cpu_id value in canister
* Mon Aug 05 2024 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.1.102-1
- Update to version 6.1.102
* Wed Jul 10 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.97-1
- Update to version 6.1.97
* Wed Jun 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 6.1.94-1
- Update to version 6.1.94
* Tue Jun 11 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.90-4
- Include External Entropy support only for X86_64.
* Mon Jun 03 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.90-3
- External entropy support.
* Mon May 20 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.90-2
- Optimize gdb commands in check_fips_canister_compatibility script
* Mon May 13 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.90-1
- Update to version 6.1.90
* Thu May 09 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.83-4
- Enable CONFIG_X86_SGX
* Wed May 08 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.83-3
- Add SEV patches back in spec file
* Sun Apr 14 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.83-2
- Patched CVE-2024-26643
* Thu Apr 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.83-1
- Update to version 6.1.83
- Fix CVE-2024-26642
* Wed Apr 10 2024  Kuntal Nayak <kuntal.nayak@broadcom.com> 6.1.81-6
- Update SBAT verification
* Wed Apr 10 2024 Srinidhi Rao <srinidhi.rao@broadcom.com> 6.1.81-5
- Defer the initialization of jitterentropy.
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
* Mon Feb 12 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 6.1.75-3
- Update canister version to 5.0.0-6.1.75-2
* Wed Jan 31 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 6.1.75-2
- Upgrade iavf to v4.9.5 and ice to 1.13.7
* Tue Jan 23 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.75-1
- Update to version 6.1.75
* Tue Jan 23 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.1.70-4
- Fix CVE-2023-6915
* Wed Jan 17 2024 Bryan Tan <bryan-bt.tan@broadcom.com> 6.1.70-3
- Fix refcount underflow in vsock
* Tue Jan 16 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.1.70-2
- Fix CVE-2024-0340
* Mon Jan 01 2024 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.70-1
- Update to version 6.1.70
* Wed Dec 20 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-14
- Increase CONFIG_LOG_BUF_SHIFT to 18
- Decrease CONFIG_LOG_CPU_MAX_BUF_SHIFT to 12
* Thu Dec 14 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-13
- Update canister to 5.0.0-6.1.62-13
* Thu Dec 14 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-12
- FIPS: Add log messages for approved and non-approved services
- Remove fips=2 logic
* Tue Dec 12 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.62-11
- Fix CVE-2023-39191
* Fri Dec 08 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.62-10
- Added self-tests for rsa-pkcs1pad in combination with sha1, sha224, sha384 and sha512
* Tue Dec 5 2023 Albert Guo <aguo@vmware.com> 6.1.62-9
- Fix race condition in v9fs_dentry_release
* Mon Nov 27 2023 Kuntal Nayak <nkuntal@vmware.com> 6.1.62-8
- Fix CVE-2023-5633
* Sat Nov 25 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-7
- Update canister to 5.0.0-6.1.62-7
* Thu Nov 23 2023 Ankit Jain <ankitja@vmware.com> 6.1.62-6
- tarfs: Fixes file permission
* Wed Nov 22 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.62-5
- Fix for CVE-2023-2176
* Tue Nov 21 2023 Keerthana K <keerthanak@vmware.com> 6.1.62-4
- Update canister to 5.0.0-6.1.62-2
* Mon Nov 20 2023 Ajay Kaher <akaher@vmware.com> 6.1.62-3
- Enabling VFIO, UIO and IOMMU support
* Sat Nov 18 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.62-2
- Fix RSA self tests
* Tue Nov 14 2023 Ankit Jain <ankitja@vmware.com> 6.1.62-1
- Update to version 6.1.62
* Mon Nov 6 2023 Albert Guo <aguo@vmware.com> 6.1.60-5
- Use iov_iter_revert() to fix offset of iov.
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
- newca: fixes and enhancements
* Thu Oct 26 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-8
- Upgrade canister to 5.0.0-6.1.56-6
* Tue Oct 24 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-7
- Added cts to crypto self-tests
- Removed rsa(pkcs1pad, sha256), rsa(pkcs1pad, sha512),
  cbc, and ctr from crypto self-tests
- Added ECC pubkey generation and verification success messages
* Fri Oct 20 2023 Albert Guo <aguo@vmware.com> 6.1.56-6
- Ported 11 9P patches (combined 2 of them) for VDFS from 4.19.y(photon3) to 6.1.y(photon5).
* Wed Oct 18 2023 Keerthana K <keerthanak@vmware.com> 6.1.56-5
- Modified ecdh-nist-p384 vector to generate ECC keypair
* Tue Oct 17 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-4
- Upgrade canister to 5.0.0-6.1.56-3
* Tue Oct 10 2023 Srish Srinivasan <ssrish@vmware.com> 6.1.56-3
- Add missing self-test vector for ecdh-nist-p384 with genkey
* Mon Oct 09 2023 Srinidhi Rao <srinidhir@vmware.com> 6.1.56-2
- Jitterentropy wrapper changes.
* Fri Oct 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.56-1
- Upgrade to 6.1.56
* Tue Oct 03 2023 Kuntal Nayak <nkunal@vmware.com> 6.1.53-8
- Kconfig to lockdown kernel in UEFI Secure Boot
* Sun Oct 01 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.53-7
- Fix for CVE-2023-42754
* Sat Sep 30 2023 Keerthana K <keerthanak@vmware.com> 6.1.53-6
- Revert crypto_test (tcrypt) config to 'm'
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
* Mon Jul 31 2023 Ajay Kaher <akaher@vmware.com> 6.1.41-2
- Fix: unconditional preserve CR4.MCE
* Thu Jul 20 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.41-1
- Update to version 6.1.41
* Mon Jul 17 2023 Keerthana K <keerthanak@vmware.com> 6.1.37-3
- Use canister version 5.0.0-6.1.37-2
* Thu Jul 06 2023 Garrett Goble <gobleg@vmware.com> 6.1.37-2
- Adding SBX kernel driver
* Tue Jul 04 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.1.37-1
- Update to version 6.1.37
* Tue Jun 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.32-1
- Update to version 6.1.32
* Wed May 31 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.1.28-2
- disable kconfig CONFIG_RAID6_PQ_BENCHMARK
* Tue May 16 2023 Ankit Jain <ankitja@vmware.com> 6.1.28-1
- Update to version 6.1.28
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-12
- Remove dracut & initramfs from requires
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-11
- Remove dracut & initramfs from requires
* Wed Apr 19 2023 Ankit Jain <ankitja@vmware.com> 6.1.10-10
- tarfs: fixes buffer overflow
* Thu Apr 13 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 6.1.10-9
- Use canister version 5.0.0-6.1.10-10
* Thu Apr 06 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.1.10-8
- Expose Photon kernel macros to simplify building out-of-tree drivers.
* Thu Mar 30 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.1.10-7
- Update drivers
- iavf: 4.8.2
- ice: 1.11.14
- i40e: 2.22.18
* Fri Mar 24 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-6
- Disable FIPS canister binary usage
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-5
- Fix initramfs trigger
* Thu Mar 16 2023 Keerthana K <keerthanak@vmware.com> 6.1.10-4
- Enable FIPS canister binary usage
* Thu Mar 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.10-3
- Fix initrd generation logic
- Add dracut, initramfs to requires
* Fri Feb 24 2023 Ankit Jain <ankitja@vmware.com> 6.1.10-2
- Exclude iavf.conf
* Wed Feb 22 2023 Bo Gan <ganb@vmware.com> 6.1.10-1
- Update to 6.1.10
* Thu Feb 16 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-8
- Update i40e driver to v2.19.3 to prevent kernel warnings
* Thu Feb 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.0.7-7
- Fix requires
* Mon Jan 30 2023 Keerthana K <keerthanak@vmware.com> 6.0.7-6
- Enable CONFIG_E1000E & CONFIG_E1000 for arm64
* Fri Jan 27 2023 Shivani Agarwal <shivania2@vmware.com> 6.0.7-5
- Enable CONFIG_DRM_I915
* Wed Jan 18 2023 Ajay Kaher <akaher@vmware.com> 6.0.7-4
- Fix aarch64 rpm build issue
* Fri Jan 13 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-3
- Fix IRQ affinities of i40e, iavf and ice drivers
* Mon Jan 09 2023 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 6.0.7-2
- Update Intel drivers i40e to v2.16.11, iavf to v4.5.3 and ice to v1.9.11
* Mon Jan 09 2023 Bo Gan <ganb@vmware.com> 6.0.7-1
- Update to 6.0.7
- common: Change from SLAB to SLUB
- common: Enable BPF/JIT
- aarch64: match configs with x86 for arch independent features.
- aarch64: disable unused platform/drivers for VM.
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.142-4
- Bump up due to change in elfutils
* Mon Nov 21 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.142-3
- Avoid extra scanning for peer host bridges when mmconfig is initialized.
* Thu Oct 20 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.142-2
- Fix build with latest toolchain
* Wed Sep 28 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.142-1
- Update to version 5.10.142
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.132-1
- Update to version 5.10.132
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-11
- Backport fixes for CVE-2022-0500
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-10
- Fix for CVE-2022-2585, CVE-2022-2586 and CVE-2022-2588
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-9
- tarfs: fix error for empty tar archive
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-8
- Fix multiple issues in tarfs
* Tue Sep 27 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-7
- Update iavf driver to v4.4.2
- Update ice driver to v1.8.3
- .config: Enable CONFIG_NET_DEVLINK=y (ice v1.8.3 needs it)
* Mon Sep 26 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-6
- .config: enable CROSS_MEMORY_ATTACH
- Add elfutils-libelf-devel required to build objtool
- vmxnet3: enable software timestamping
* Fri Sep 23 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.118-5
- .config: disable kernel accounting for memory cgroups
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
* Wed Sep 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-4
- .config: Increase kernel log buffer size to fix regression.
* Tue Sep 20 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-3
- Fix for CVE-2022-1016
* Mon Sep 19 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-2
- Fix SEV and Hypercall alternative inst. patches
* Thu Sep 15 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.103-1
- Update to version 5.10.103
* Thu Sep 15 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-7
- Reduce kernel .data section by configuring smaller kernel log buffer (16)
- Speedup algos registration in non-fips mode
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-6
- vtarfs: fix multiple issues
- tarfs: support for hardlink, fix uid/gid/mode issues
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
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-7
- Update ptp_vmw with provider mode support
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-6
- Fix CVE-2021-4155 and CVE-2021-4204
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-5
- crypto_self_test and broken kattest module enhancements
- FIPS: Add module signing for crypto modules
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-4
- mm: fix percpu allocation for memoryless nodes
- pvscsi: fix disk detection issue
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-3
- remove lvm in add-drivers list
- lvm drivers are built as part of dm-mod
* Tue Sep 13 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-2
- tarfs: Fix binary execution issue
* Mon Sep 12 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-1
- Update to version 5.10.83
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-17
- Scriptlets fixes and improvements
* Fri Jul 29 2022 Tejaswini Jayaramaiah <jtejaswini@vmware.com> 5.10.78-16
- Enable CONFIG_CGROUP_BPF in config to run containers with cgroup v2
* Wed Jun 29 2022 Keerthana K <keerthanak@vmware.com> 5.10.78-15
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-14
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Tue May 31 2022 Ajay Kaher <akaher@vmware.com> 5.10.78-13
- initialize MMCONFIG, if already not initialized
* Mon Apr 18 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-12
- Add objtool to the -devel package.
- Reduce kernel .data section by configuring smaller kernel log buffer
- .config(x86_64): enable amdgpu driver as a module
* Tue Apr 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.78-11
- Enable CONFIG_EXT2_FS_XATTR & related parameters
* Mon Feb 28 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.10.78-10
- Port non-acpi hotplug support patch to 5.10.x
* Tue Feb 01 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-9
- Reduce kernel .text size by ~40% by removing .entry.text alignment.
* Tue Jan 25 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.78-8
- .config: enable squashfs module, enable crypto user api rng.
* Wed Dec 01 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-7
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Nov 30 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-6
- Correct the config file for linux-esx on arm machine
* Tue Nov 23 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.78-5
- tarfs: A new readonly filesystem to mount tar archive
* Fri Nov 19 2021 Keerthana K <keerthanak@vmware.com> 5.10.78-4
- Remove vmci and vmw_balloon patches
- Update Hypervisor detection patch with review comments addressed
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.10.78-3
- compile with openssl 3.0.0
* Mon Nov 08 2021 Keerthana K <keerthanak@vmware.com> 5.10.78-2
- Add out-of-tree i40e, iavf and ice drivers.
* Mon Nov 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.78-1
- Update to version 5.10.78
* Thu Oct 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.75-1
- Update to version 5.10.75
* Thu Oct 21 2021 Keerthana K <keerthanak@vmware.com> 5.10.61-7
- Arm64 VMware Hypervisor features
- Arm64 support for vmw_pvscsi, vmw_vmci and vmw_balloon
- vmxnet3: build only for x86 and arm64
* Thu Oct 21 2021 Keerthana K <keerthanak@vmware.com> 5.10.61-6
- Add arm64 support
* Mon Oct 18 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.61-5
- initramfs: large files support for newca
* Wed Oct 06 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-4
- vtarfs: Fix memory allocation for entry pages
* Fri Sep 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-3
- vtarfs: Added support for LongFilename/LongLink
* Tue Sep 07 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-2
- vtarfs: Fix crash in vtarfs_file_read_iter()
* Fri Aug 27 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-1
- Update to version 5.10.61
* Wed Aug 25 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.52-3
- Enable ptp_vmw module (CONFIG_PTP_1588_CLOCK_VMW) in the config.
* Mon Aug 09 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-2
- Port crx patches
* Thu Aug 05 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
- Update to version 5.10.52
* Wed Jul 28 2021 Ankit Jain <ankitja@vmware.com> 5.10.46-3
- vtarfs: Fixed multiple mount executable issue,
-         Fixed fault handler
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
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
- Fix for CVE-2021-23133
* Wed May 12 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
- .config: Enable Netfilter modules required for NFT support
- .config: Enable Bonding driver support, NET_TEAM, NET_VRF
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
- Remove hmac(sha224) from broken kat test.
* Thu Apr 15 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
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
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-14
- Enable FIPS canister
* Fri Feb 19 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-13
- Enable CONFIG_ISCSI_TCP support
* Fri Feb 19 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-12
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Fri Feb 19 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-11
- Added SEV-ES improvement patches
* Thu Feb 18 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-10
- Disable fips canister.
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-9
- Enable CONFIG_WDAT_WDT
* Thu Feb 18 2021 Ajay Kaher <akaher@vmware.com> 5.10.4-8
- lower the loglevel for floppy driver
* Mon Feb 15 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-7
- Enable CONFIG_NF_TABLES support
* Thu Feb 11 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-6
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Wed Feb 03 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-5
- Replaced syscalls routines based on user space address
- Removed set_fs() calls
* Thu Jan 28 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-4
- Use secure FIPS canister.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-3
- Enabled CONFIG_WIREGUARD
* Mon Jan 25 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-2
- Build kernel with FIPS canister.
* Wed Jan 06 2021 Bo Gan <ganb@vmware.com> 5.10.4-1
- Update to 5.10.4
- Drop out-of-tree SEV-ES functional patches (already upstreamed).
* Thu Dec 03 2020 Alexey Makhalov <amakhalov@vmware.com> 5.9.0-8
- halt_on_panic kernel cmdline.
- Improve no ACPI poweroff patch to support direct boot.
- .config: enable CONFIG_POWER_RESET_PIIX4_POWEROFF.
* Wed Nov 18 2020 Vikash Bansal <bvikas@vmware.com> 5.9.0-7
- Mark BAR0 (at offset 0x10) for PCI device 15ad:07b0 (VMXNET3) as variable
* Thu Nov 12 2020 Ajay Kaher <akaher@vmware.com> 5.9.0-6
- .config: support for floppy disk and ch341 usb to serial
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-5
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-25704
* Tue Nov 03 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-3
- Remove the support of fipsify and hmacgen
* Tue Oct 27 2020 Srinidhi Rao <srinidhir@vmware.com> 5.9.0-2
- Enable vtarfs support as module
* Mon Oct 19 2020 Bo Gan <ganb@vmware.com> 5.9.0-1
- Update to 5.9.0
* Thu Oct 08 2020 Ankit Jain <ankitja@vmware.com> 5.9.0-rc7.2
- Added vtar Support.
- Disabled by default, Enable CONFIG_VTAR as builtin only
* Wed Sep 30 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
- Update to version 5.9.0-rc7
* Mon Sep 21 2020 Bo Gan <ganb@vmware.com> 5.9.0-rc4.1
- Update to 5.9.0-rc4
- AMD SEV-ES Support
* Tue Sep 8 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.127-4
- Enable sysrq magic in config
* Mon Jul 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.127-3
- Fix CVE-2020-14331
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 4.19.127-2
- Mass Removal Python2
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.115-5
- Enabled CONFIG_BINFMT_MISC
* Wed Jun 03 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.115-4
- fs/9p: local lock support
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-3
- Add patch to fix CVE-2019-18885
* Mon Jun 01 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-2
- Keep modules of running kernel till next boot
* Fri May 29 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.115-1
- initramfs: zero-copy support
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.112-9
- Add patch to fix CVE-2020-10711
* Wed May 06 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-8
- Hardcoded the value of BARs in PCI_Probe for 2 more pci devices
* Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-7
- Photon-checksum-generator version update to 1.1.
* Fri Apr 24 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-6
- Modified PCI Probe patch to store hardcoded values in lookup table
* Thu Apr 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.112-5
- Fix __modules_install_post to skip compression for certain modules.
* Wed Apr 22 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-4
- Corrected number of bars for "LSI Logic" and typepo in is_known_device call
* Wed Apr 15 2020 Vikash Bansal <bvikas@vmware.com> 4.19.112-3
- HMAC-SHA256 digest of hmac_generator module moved to hmacgen package
* Tue Apr 14 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.112-2
- Refactor PCI probe patch (03-pci-probe.patch)
* Wed Apr 08 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.112-1
- Update to version 4.19.112
* Wed Apr 08 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.104-3
- Improve hardcodded poweroff (03-poweroff.patch)
* Tue Mar 31 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-2
- hmac generation of crypto modules and initrd generation changes if fips=1
* Wed Mar 25 2020 Vikash Bansal <bvikas@vmware.com> 4.19.104-1
- Update to version 4.19.104
* Mon Mar 16 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-8
- Adding Enhances depedency to hmacgen.
* Fri Mar 06 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.97-7
- 9p: file attributes caching support (cache=stat)
* Wed Mar 04 2020 Vikash Bansal <bvikas@vmware.com> 4.19.97-6
- Backporting of patch continuous testing of RNG from urandom
* Fri Feb 28 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-5
- Enable CONFIG_CRYPT_TEST for FIPS.
* Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.19.97-4
- Fix CVE-2019-16234
* Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-3
- Add photon-checksum-generator source tarball and remove hmacgen patch.
- Exclude hmacgen.ko from base package.
* Wed Jan 29 2020 Keerthana K <keerthanak@vmware.com> 4.19.97-2
- Update tcrypt to test drbg_pr_sha256 and drbg_nopr_sha256.
- Update testmgr to add drbg_pr_ctr_aes256 test vectors.
* Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.97-1
- Update to version 4.19.97
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.87-5
- Enable DRBG HASH and DRBG CTR support.
* Mon Jan 06 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.87-4
- Enable CONFIG_NF_CONNTRACK_ZONES
* Thu Jan 02 2020 Keerthana K <keerthanak@vmware.com> 4.19.87-3
- Modify tcrypt to remove tests for algorithms that are not supported in photon.
- Added tests for DH, DRBG algorithms.
* Fri Dec 20 2019 Keerthana K <keerthanak@vmware.com> 4.19.87-2
- Update fips Kat tests.
* Fri Dec 06 2019 Ajay Kaher <akaher@vmware.com> 4.19.87-1
- Update to version 4.19.87
* Tue Dec 03 2019 Keerthana K <keerthanak@vmware.com> 4.19.84-3
- Adding hmac sha256/sha512 generator kernel module for fips.
* Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.19.84-2
- Fix CVE-2019-19062, CVE-2019-19066, CVE-2019-19072,
- CVE-2019-19073, CVE-2019-19074, CVE-2019-19078
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.84-1
- Update to version 4.19.84
- Fix CVE-2019-18814
* Fri Nov 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Update to version 4.19.82
* Thu Nov 07 2019 Jorgen Hansen (VMware) <jhansen@vmware.com> 4.19.79-2
- Fix vsock QP detach with outgoing data
* Tue Oct 15 2019 Ajay Kaher <akaher@vmware.com> 4.19.79-1
- Update to version 4.19.79
- Fix CVE-2019-17133
* Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-4
- Recreate /dev/root in init
* Mon Oct 14 2019 Bo Gan <ganb@vmware.com> 4.19.76-3
- Enable IMA with SHA256 as default hash algorithm
* Thu Oct 10 2019 Harinadh D <hdommaraju@vmware.com> 4.19.76-2
- Adding lvm and dm-mod modules to support root as lvm
* Wed Oct 02 2019 Ajay Kaher <akaher@vmware.com> 4.19.76-1
- Update to version 4.19.76
* Mon Sep 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.72-1
- Update to version 4.19.72
* Thu Sep 05 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-2
- Avoid oldconfig which leads to potential build hang
* Fri Aug 30 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.69-1
- Update to version 4.19.69
* Fri Aug 23 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.65-3
- .config: Enable CONFIG_IP_VS_WRR, CONFIG_IP_VS_SH, CONFIG_FB_EFI, CONFIG_TCG_TIS_CORE
* Tue Aug 13 2019 Daniel Müller <danielmuller@vmware.com> 4.19.65-2
- Add patch "Remove OOM_SCORE_ADJ_MAX limit check"
* Tue Aug 06 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.65-1
- Update to version 4.19.65
- Fix CVE-2019-1125 (SWAPGS)
* Tue Jul 30 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-4
- Fix postun script.
* Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-3
- Fix 9p vsock 16bit port issue.
* Fri Jun 21 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.52-2
- Use LZ4 compression and enable VMXNET3 as built-in for linux-esx
* Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
- Update to version 4.19.52
- Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
- CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
* Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
- Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
- mulitple kernels are installed and current linux kernel is removed.
* Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
- Update to version 4.19.40
* Fri May 03 2019 Ajay Kaher <akaher@vmware.com> 4.19.32-3
- Enable SELinux kernel config
* Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
- Fix CVE-2019-10125
* Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
- Update to version 4.19.32
* Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
- Update to version 4.19.29
* Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
- Update to version 4.19.26
* Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-2
- Fix CVE-2019-8912
* Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
- Update to version 4.19.15
- .config: Enable USB_SERIAL and USB_ACM
* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
- Additional security hardening options in the config.
* Tue Jan 08 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-3
- Fix crash on cpu hot-add.
* Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-2
- Add out-of-tree patches from AppArmor and enable it by default.
* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6
* Thu Nov 29 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
- Fix BAR4 is zero issue for IDE devices
* Thu Nov 15 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
- Adding BuildArch
* Thu Nov 08 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.1-1
- Update to version 4.19.1
* Mon Sep 24 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9
* Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
- Update to version 4.14.67
* Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-3
- Add rdrand-based RNG driver to enhance kernel entropy.
* Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-2
- Add full retpoline support by building with retpoline-enabled gcc.
* Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
- Update to version 4.14.54
* Fri Feb 02 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
- Version update
* Tue Dec 19 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-2
- Enable audit support (CONFIG_AUDIT=y)
* Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
- Version update
* Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
- Version update
* Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
- Version update
* Wed Oct 25 2017 Anish Swaminathan <anishs@vmware.com> 4.9.53-5
- Enable x86 vsyscall emulation
* Tue Oct 17 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-4
- Enable vsyscall emulation
- Do not use deprecated -q depmod option
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
* Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
- Version update
- [feature] new sysctl option unprivileged_userns_clone
* Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
- [bugfix] Do not fallback to syscall from VDSO on clock_gettime(MONOTONIC)
- Fix CVE-2017-7542
* Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
- Version update
* Wed Jul 26 2017 Bo Gan <ganb@vmware.com> 4.9.38-3
- Fix initramfs triggers
* Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
- Disable scheduler beef up patch
* Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
- [feature] IP tunneling support (CONFIG_NET_IPIP=m)
- Fix CVE-2017-11176 and CVE-2017-10911
* Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-2
- Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
* Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
- [feature] DM Delay target support
- Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
* Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
- Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
* Thu Jun 1 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-2
- [feature] ACPI NFIT support (for PMEM type 7)
* Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
- Fix CVE-2017-7487 and CVE-2017-9059
* Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
- Enable IPVLAN module.
* Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
- .config: built ATA drivers in a kernel
* Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
- New pci=scan_all cmdline parameter to verify hardcoded pci-probe values
- pci-probe added more known values
- vmw_balloon late initcall
* Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
- Version update
- Use ordered rdtsc in clocksource_vmware
- .config: added debug info
- Removed version suffix from config file name
* Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
- Support dynamic initrd generation
* Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
- Fix CVE-2017-6874 and CVE-2017-7618.
- .config: build nvme and nvme-core in kernel.
* Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
- Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
- .config: enable PMEM support
- .config: disable vsyscall
* Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
- Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
- .config: added CRYPTO_FIPS and SYN_COOKIES support.
* Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
- Update to linux-4.9.2 to fix CVE-2016-10088
* Wed Dec 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-3
- .config: CONFIG_IPV6_MULTIPLE_TABLES=y
* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
- BuildRequires Linux-PAM-devel
* Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
- Update to linux-4.9.0
* Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-4
- net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
* Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
- Expand `uname -r` with release number
- Compress modules
* Tue Nov 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
- Added btrfs module
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
- .config: add ip set support
- .config: add ipvs_{tcp,udp} support
- .config: add cgrup_{hugetlb,net_prio} support
* Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
- Update to linux-4.4.31
* Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-2
- .config: add ipvs modules for docker swarm
- .config: serial driver built in kernel
- serial-8250-do-not-probe-U6-16550A-fifo-size.patch - faster boot
* Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
- Update to linux-4.4.26
* Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-7
- net-add-recursion-limit-to-GRO.patch
* Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
- ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
- tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
* Thu Oct  6 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
- .config: added ADM PCnet32 support
- vmci-1.1.4.0-use-32bit-atomics-for-queue-headers.patch
- vmci-1.1.5.0-doorbell-create-and-destroy-fixes.patch
- late_initcall for vmw_balloon driver
- Minor fixed in pv-ops patchset
* Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
- Package vmlinux with PROGBITS sections in -debuginfo subpackage
* Wed Sep 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
- Add PCIE hotplug support
- Switch processor type to generic
* Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
- Add -release number for /boot/* files
- Fixed generation of debug symbols for kernel modules & vmlinux
* Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
- Update to linux-4.4.20
- keys-fix-asn.1-indefinite-length-object-parsing.patch
* Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
- vmxnet3 patches to bumpup a version to 1.4.8.0
* Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
- .config: added NVME blk dev support
* Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
- Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
* Wed Jul 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
- .config: added cgroups for pids,mem and blkio
* Mon Jul 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-7
- .config: added ip multible tables support
* Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
- patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
- .config: disable rt group scheduling - not supported by systemd
* Fri May 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-5
- patch: REVERT-sched-fair-Beef-up-wake_wide.patch
* Wed May 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-4
- .config: added net_9p and 9p_fs
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-3
- GA - Bump release of all rpms
* Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-2
- Added patches to fix CVE-2016-3134, CVE-2016-3135
* Fri May 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
- Update to linux-4.4.8
- Added net-Drivers-Vmxnet3-set-... patch
- Added e1000e module
* Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
- Support kmsg dumping to vmware.log on panic
- sunrpc: xs_bind uses ip_local_reserved_ports
* Thu Mar 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
- Apply photon8 config (+stack protector regular)
- pv-ops patch: added STA support
- Added patches from generic kernel
* Wed Mar 09 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-17
- Enable ACPI hotplug support in kernel config
* Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-16
- veth patch: don’t modify ip_summed
* Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
- Double tcp_mem limits, patch is added.
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-14
- Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
* Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
- Fix for CVE-2016-0728
* Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-12
- CONFIG_HZ=250
- Disable sched autogroup.
* Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-11
- Remove rootfstype from the kernel parameter.
* Tue Dec 15 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
- Skip rdrand reseed to improve boot time.
- .config changes: jolietfs(m), default THP=always, hotplug_cpu(m)
* Tue Nov 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
- nordrand cmdline param is removed.
- .config: + serial 8250 driver (M).
* Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
- Change the linux image directory.
* Tue Nov 10 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-7
- Get LAPIC timer frequency from HV, skip boot time calibration.
- .config: + dummy net driver (M).
* Mon Nov 09 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-6
- Rename subpackage dev -> devel.
- Added the build essential files in the devel subpackage.
- .config: added genede driver module.
* Wed Oct 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-5
- Import patches from kernel2 repo.
- Added pv-ops patch (timekeeping related improvements).
- Removed unnecessary cmdline params.
- .config changes: elevator=noop by default, paravirt clock enable,
    initrd support, openvswitch module, x2apic enable.
* Mon Sep 21 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-4
- CDROM modules are added.
* Thu Sep 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-3
- Fix for 05- patch (SVGA mem size)
- Compile out: pci hotplug, sched smt.
- Compile in kernel: vmware balloon & vmci.
- Module for efi vars.
* Fri Sep 4 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-2
- Hardcoded poweroff (direct write to piix4), no ACPI is required.
- sd.c: Lower log level for "Assuming drive cache..." message.
* Tue Sep 1 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-1
- Update to linux-4.2.0. Enable CONFIG_EFI
* Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-5
- Added MD/LVM/DM modules.
- Pci probe improvements.
* Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-4
- Use photon.cfg as a symlink.
* Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-3
- Added environment file(photon.cfg) for a grub.
* Tue Aug 11 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-2
- Added pci-probe-vmware.patch. Removed unused modules. Decreased boot time.
* Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-1
- Initial commit. Use patchset from Clear Linux.
