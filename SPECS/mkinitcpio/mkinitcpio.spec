Summary:       Modular initramfs image creation utility
Name:          mkinitcpio
Version:       34
Release:       3%{?dist}
URL:           https://projects.archlinux.org/mkinitcpio.git/
Group:         System Environment/Development
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://projects.archlinux.org/mkinitcpio.git/snapshot/%{name}-%{version}.tar.gz
%define sha512 %{name}=38a80bb9e769b9fbf143c91fc52af1b29dfed81f05a3a9c4bb52d15a5e8a37fe55185ecc2218bcf6d13ac77e510803ee27314430e7b161a565b0e698e275f690

Source1: license.txt
%include %{SOURCE1}

Patch0:        mkinitcpio-shutdown-ramfs.service.patch

BuildRequires: asciidoc3
BuildRequires: git
BuildRequires: python3-devel
BuildRequires: python3-xml
BuildRequires: docbook-xsl
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel

BuildArch:     noarch

%description
Multi-format archive and compression library

%prep
%autosetup -p0

%build
for i in "hooks/*" ; do
  sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" $i
done
sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" init
sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" shutdown
sed -i "s/a2x/a2x3 --verbose --no-xmllint/" Makefile

%make_build

%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*
%{_bindir}/*
%{_sysconfdir}/*
%{_datadir}/*

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 34-3
- Release bump for SRP compliance
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 34-2
- Bump version as a part of libxml2 upgrade
* Fri Dec 23 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 34-1
- Update to version 34
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 31-3
- Update release to compile with python 3.11
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 31-2
- Bump version as a part of libxslt upgrade
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 31-1
- Automatic Version Bump
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 30-2
- Bump version as a part of libxslt upgrade
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 30-1
- Automatic Version Bump
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 28-1
- Automatic Version Bump
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 24-3
- Build with python3
- Mass removal python2
* Fri Jan 18 2019 Alexey Makhalov <amakhalov@vmware.com> 24-2
- Added buildRequires python2.
* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 24-1
- Update to version 24
* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 23-3
- fix directory create in shutdown service
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 23-2
- Fix arch
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 23-1
- Update package version
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 19-1
- Updated to new version.
* Sat Jul 11 2015 Touseef Liaqat <tliaqat@vmware.com> 18-2
- Remove ash dependency
* Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 18-1
- Initial build.  First version
