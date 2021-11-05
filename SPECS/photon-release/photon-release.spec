Summary:        Photon release files
Name:           photon-release
Version:        3.0
Release:        6%{?dist}
License:        Apache License
Group:          System Environment/Base
URL:            https://vmware.github.io/photon/
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-3.0.tar.gz
%define sha1 %{name}=ced639518d32f9ac8ff00a71853812057db3ab3c

Source1:        lsb_release

Provides:       system-release
Provides:       system-release(%{version})
Provides:       system-release(releasever) = %{version}

BuildArch:      noarch

%description
Photon release files such as yum configs and other %{_sysconfdir}/ release related files

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_libdir}

mkdir -p %{buildroot}%{_bindir}
cp %{SOURCE1} %{buildroot}%{_bindir}
chmod +x %{buildroot}%{_bindir}/lsb_release

echo "VMware Photon OS %{photon_release_version}" > %{buildroot}%{_sysconfdir}/%{name}
echo "PHOTON_BUILD_NUMBER=%{photon_build_number}" >> %{buildroot}%{_sysconfdir}/%{name}

cat > %{buildroot}%{_sysconfdir}/lsb-release <<- "EOF"
DISTRIB_ID="VMware Photon OS"
DISTRIB_RELEASE="%{photon_release_version}"
DISTRIB_CODENAME=Photon
DISTRIB_DESCRIPTION="VMware Photon OS %{photon_release_version}"
EOF

version_id=`echo %{photon_release_version} | grep -o -E '[0-9]+.[0-9]+'`
cat > %{buildroot}%{_libdir}/os-release << EOF
NAME="VMware Photon OS"
VERSION="%{photon_release_version}"
ID=photon
VERSION_ID=$version_id
PRETTY_NAME="VMware Photon OS/Linux"
ANSI_COLOR="1;34"
HOME_URL="https://vmware.github.io/photon/"
BUG_REPORT_URL="https://github.com/vmware/photon/issues"
EOF

ln -sv ..%{_libdir}/os-release %{buildroot}%{_sysconfdir}/os-release

cat > %{buildroot}%{_sysconfdir}/issue <<- EOF
Welcome to Photon %{photon_release_version} (\m) - Kernel \r (\l)
EOF

cat > %{buildroot}%{_sysconfdir}/issue.net <<- EOF
Welcome to Photon %{photon_release_version} (%m) - Kernel %r (%t)
EOF

%post

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/lsb_release
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/lsb-release
%config(noreplace) %{_libdir}/os-release
%config(noreplace) %{_sysconfdir}/os-release
%config(noreplace) %{_sysconfdir}/issue
%config(noreplace) %{_sysconfdir}/issue.net

%changelog
* Wed Oct 27 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.0-6
- Add lsb_release
* Wed Feb 26 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0-5
- Fixed Build Number Issue
* Sat Jan 04 2020 Neal Gompa <ngompa13@gmail.com> 3.0-4
- Fix issue files to not require arch mangling
- Add system-release Provides for generic distroverpkg identifying name
* Tue May 7 2019 Michelle Wang <michellew@vmware.com> 3.0-3
- Add sources0 for OSSTP tickets
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
