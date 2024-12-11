Summary:        Tools and Utilities for interaction with SCSI devices.
Name:           sg3_utils
Version:        1.47
Release:        3%{?dist}
URL:            https://github.com/doug-gilbert/sg3_utils
Group:          System/Tools.
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://sg.danny.cz/sg/p/%{name}-%{version}.tar.xz
%define sha512 %{name}=ef072b8f0012d0944e21d2134aff7125e24ea24d1cbbb1aa79160e844f9a60236f1e244437a3bc08a22a7e99f613adad4a05ae5cc3916ded5a72d162cd3aa163

Source1: license.txt
%include %{SOURCE1}

Patch0:         0001-sg3_utils-Fix-issue-with-rescan-scsi-bus.sh-removing.patch

Provides:       sg_utils

BuildRequires:  lua-devel

%description
Linux tools and utilities to send commands to SCSI devices.

%package -n     libsg3_utils-devel
Summary:        Devel pacjage for sg3_utils.
Group:          Development/Library.
Requires:       %{name} = %{version}-%{release}

%description -n libsg3_utils-devel
Package containing static library object for development.

%prep
%autosetup -p1

%build
%configure

%install
%make_install %{?_smp_mflags}
install -m 755 scripts/scsi_logging_level %{buildroot}%{_bindir}
install -m 755 scripts/rescan-scsi-bus.sh %{buildroot}%{_bindir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*
%{_libdir}/libsgutils2*.so.*

%files -n libsg3_utils-devel
%defattr(-,root,root)
%{_libdir}/libsgutils2.a
%{_libdir}/libsgutils2.so
%{_includedir}/scsi/*

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.47-3
- Release bump for SRP compliance
* Tue Jun 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.47-2
- Bump version as a part of lua upgrade
* Tue Apr 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.47-1
- Upgrade to v1.47
* Thu Apr 13 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.46-2
- fix issue with rescan-scsi-bus.sh removing hard disks
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 1.46-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.44-1
- Automatic Version Bump
* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.43-2
- Fix compilation issue against glibc-2.28
* Tue Oct 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.43-1
- Update to v1.43
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.42-2
- GA - Bump release of all rpms
* Thu Apr 14 2016 Kumar Kaushik <kaushikk@vmware.com> 1.42-1
- Initial build. First version
