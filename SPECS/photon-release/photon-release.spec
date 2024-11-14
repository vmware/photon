Summary:        Photon release files
Name:           photon-release
Version:        5.0
Release:        5%{?dist}
Group:          System Environment/Base
URL:            https://vmware.github.io/photon
Vendor:         VMware, Inc.
Distribution:   Photon

Source1: lsb_release

Source2: license.txt
%include %{SOURCE2}

Provides:       system-release
Provides:       system-release(%{version})
Provides:       system-release(releasever) = %{version}

Requires:       bash

BuildArch:      noarch

%description
Photon release files such as yum configs and other %{_sysconfdir}/ release related files

%install
mkdir -m755 -p %{buildroot}{%{_sysconfdir},%{_libdir}}

install -D -m 755 %{SOURCE1} %{buildroot}%{_bindir}/lsb_release

cat > %{buildroot}%{_sysconfdir}/photon-release <<- "EOF"
VMware Photon OS %{photon_release_version}
PHOTON_BUILD_NUMBER=%{photon_build_number}
EOF

cat > %{buildroot}%{_sysconfdir}/lsb-release <<- "EOF"
DISTRIB_ID="VMware Photon OS"
DISTRIB_RELEASE="%{photon_release_version}"
DISTRIB_CODENAME=Photon
DISTRIB_DESCRIPTION="VMware Photon OS %{photon_release_version}"
EOF

version_id=$(echo %{photon_release_version} | grep -o -E '[0-9]+.[0-9]+')
cat > %{buildroot}%{_libdir}/os-release << EOF
NAME="VMware Photon OS"
VERSION="%{photon_release_version}"
ID=photon
VERSION_ID=${version_id}
PRETTY_NAME="VMware Photon OS/Linux"
ANSI_COLOR="1;34"
HOME_URL="https://vmware.github.io/photon/"
BUG_REPORT_URL="https://github.com/vmware/photon/issues"
EOF

ln -srv %{buildroot}%{_libdir}/os-release %{buildroot}%{_sysconfdir}/os-release

cat > %{buildroot}%{_sysconfdir}/issue <<- EOF
Welcome to Photon %{photon_release_version} (\m) - Kernel \r (\l)
EOF

cat > %{buildroot}%{_sysconfdir}/issue.net <<- EOF
Welcome to Photon %{photon_release_version} (%m) - Kernel %r (%t)
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %attr(0755,-,-) %{_libdir}
%dir %attr(0755,-,-) %{_bindir}
%dir %attr(0755,-,-) %{_sysconfdir}
%attr(0755,-,-) %{_bindir}/lsb_release
%config(noreplace) %attr(0644,-,-) %{_sysconfdir}/photon-release
%config(noreplace) %attr(0644,-,-) %{_sysconfdir}/lsb-release
%config(noreplace) %attr(0644,-,-) %{_libdir}/os-release
%config(noreplace) %{_sysconfdir}/os-release
%config(noreplace) %attr(0644,-,-) %{_sysconfdir}/issue
%config(noreplace) %attr(0644,-,-) %{_sysconfdir}/issue.net

%changelog
* Thu Nov 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-5
- Fix file and directory permissions
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 5.0-4
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-3
- Release bump for SRP compliance
* Tue Jan 17 2023 Tapas Kundu <tkundu@vmware.com> 5.0-2
- Requires bash
* Wed Dec 21 2022 Tapas Kundu <tkundu@vmware.com> 5.0-1
- Update to 5.0
* Wed Oct 27 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.0-2
- Add lsb_release
* Wed Oct 07 2020 Anish Swaminathan <anishs@vmware.com> 4.0-1
- Update to 4.0
* Wed Sep 23 2020 Michelle Wang <michellew@vmware.com> 3.0-4
- Add sources0 for OSSTP tickets
* Sat Jan 04 2020 Neal Gompa <ngompa13@gmail.com> 3.0-3
- Fix issue files to not require arch mangling
- Add system-release Provides for generic distroverpkg identifying name
* Fri Sep 28 2018 Ajay Kaher <akaher@vmware.com> 3.0-2
- Fix for aarch64
* Mon Sep 24 2018 Anish Swaminathan <anishs@vmware.com> 3.0-1
- Update to 3.0
* Thu Jul 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0-1
- update to 2.0
* Wed Nov 30 2016 Anish Swaminathan <anishs@vmware.com> 1.0-7
- Upgrade photon repo
* Fri Nov 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-6
- Remove requires for rpm
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-5
- GA - Bump release of all rpms
* Mon Apr 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-4
- Split up repo and gpg key files to photon-repos
* Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-3
- yum repo gpgkey to VMWARE-RPM-GPG-KEY.
* Wed Mar 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-2
- Add revision to photon-release
* Mon Jan 11 2016 Anish Swaminathan <anishs@vmware.com> 1.0-1
- Reset version to match with Photon version
* Mon Jan 04 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4
- Adding photon-extras.repo
* Thu Nov 19 2015 Anish Swaminathan <anishs@vmware.com> 1.3-1
- Upgrade photon repo
* Fri Aug 14 2015 Sharath George <sharathg@vmware.com> 1.2
- Install photon repo links
* Wed Jun 17 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1
- Install photon key
