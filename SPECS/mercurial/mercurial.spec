Summary:        A free, distributed source control management tool.
Name:           mercurial
Version:        6.3.1
Release:        2%{?dist}
URL:            https://www.mercurial-scm.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.mercurial-scm.org/release/%{name}-%{version}.tar.gz
%define sha512  %{name}=99cd77c25e6c7f064ea9b631a8632b6020cb012c2f5a8c1da371ed413a4f984d04f8c293f551f890bbf084f840d7406aa25956f016ff2596173cd2f1f834873b

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-pip
Requires:       python3

%description
Mercurial is a distributed source control management tool similar to Git and Bazaar.
Mercurial is written in Python and is used by projects such as Mozilla and Vim.

%prep
%autosetup

%build
ln -sf /usr/bin/python3 /usr/bin/python
make %{?_smp_mflags} build

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{_bindir}
%py3_install

cat >> %{buildroot}/.hgrc << "EOF"
[ui]
username = "$(id -u)"
EOF

%check
sed -i '1087,1088d' tests/test-obsolete.t
sed -i '54,56d' tests/test-clonebundles.t
sed -i '54i\ \ abort:\ stream:\ not\ a\ Mercurial\ bundle' tests/test-clonebundles.t
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
/.hgrc
%{_bindir}/hg
%{python3_sitelib}/*
%{_datadir}/bash-completion/completions/hg
%{_datadir}/zsh/site-functions/_hg

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 6.3.1-2
- Release bump for SRP compliance
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 6.3.1-1
- Automatic Version Bump
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 6.2.1-2
- Update release to compile with python 3.11
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 6.2.1-1
- Automatic Version Bump
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 6.1.1-1
- Automatic Version Bump
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 5.8-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 5.7.1-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 5.5.1-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 5.5-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 5.4-1
- Upgrade to 5.4
- Build with python3
- Mass removal python2
* Mon May 06 2019 Keerthana K <keerthanak@vmware.com> 4.7.1-3
- Fix CVE-2018-17983
* Thu Oct 25 2018 Sujay G <gsujay@vmware.com> 4.7.1-2
- Disable zstd
* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.7.1-1
- Update to version 4.7.1
* Tue Oct 17 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-1
- Update verion to 4.3.3 for CVE-2017-1000115, CVE-2017-1000116.
* Fri Aug 11 2017 Rongrong Qiu <rqiu@vmware.com> 4.1-4
- update error info in make check for bug 1900338
* Fri Jun 16 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1-3
- Use python2 explicitly while building
* Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 4.1-2
- Apply CVE-2017-9462 patch
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.1-1
- Update package version
* Sun Jan 22 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-6
- Install with setup.py.
* Tue Nov 22 2016 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-5
- Apply patches for CVE-2016-3068, CVE-2016-3069, CVE-2016-3105
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 3.7.1-4
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.7.1-3
- GA - Bump release of all rpms
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 3.7.1-2
- Edit postun script.
* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.7.1-1
- Updating Version.
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.1.2-4
- Edit post script.
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 3.1.2-3
- Change path to /var/opt.
* Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 3.1.2-2
- /etc/profile.d permission fix
* Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 3.1.2-1
- Initial build.  First version
