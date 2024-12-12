Summary:    Networking Tools
Name:       net-tools
Version:    2.10
Release:    2%{?dist}
URL:        https://github.com/ecki/net-tools
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/ecki/net-tools/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=d35bc3e233fa1aae007222516ce04a0c882632d6b3c55ca0ce33123225a6ccd7144b39059b96690b613a31164f7bab536ac85458d2d94596b672b018c5762821

Source1: net-tools-config.h
Source2: net-tools-config.make

Source3: license.txt
%include %{SOURCE3}

Conflicts: toybox < 0.8.2-2

%description
The Net-tools package is a collection of programs for controlling the network subsystem of the Linux kernel.

%prep
%autosetup -p1

%build
cp %{SOURCE1} config.h
cp %{SOURCE2} config.make

# make doesn't support _smp_mflags
yes "" | make config

# make doesn't support _smp_mflags
make

%install
# make doesn't support _smp_mflags
make BASEDIR=%{buildroot}%{_usr} installbin
# make doesn't support _smp_mflags
make BASEDIR=%{buildroot} installdata

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 2.10-2
- Release bump for SRP compliance
* Mon Sep 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.10-1
- Upgrade to v2.10
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.60-13
- Fix binary path
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 1.60-12
- Do not conflict with toybox >= 0.8.2-2
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 1.60-11
- Added conflicts toybox
* Wed Dec 14 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-10
- Fix compilation issue with linux-4.9
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-9
- Remove iputils deps.
* Tue Oct 04 2016 ChangLee <changLee@vmware.com> 1.60-8
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.60-7
- GA - Bump release of all rpms
* Thu Feb 4 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-6
- Apply all patches from 1.60-26ubuntu1.
* Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-5
- Added net-tools-1.60-manydevs.patch
* Fri Nov 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.60-4
- Added ipv6 support. Include hostname and dnshostname.
* Thu Oct 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.60-3
- Added changes to replace inetutils with net-tools
* Thu Jul 30 2015 Divya Thaluru <dthaluru@vmware.com> 1.60-2
- Disable building with parallel threads
* Mon Jul 13 2015 Divya Thaluru <dthaluru@vmware.com> 1.60-1
- Initial build. First version
