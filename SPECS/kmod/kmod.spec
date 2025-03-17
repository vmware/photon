Summary:        Utilities for loading kernel modules
Name:           kmod
Version:        34.1
Release:        1%{?dist}
URL:            http://www.kernel.org/pub/linux/utils/kernel/kmod
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel
BuildRequires:  gtk-doc

Requires: xz-libs
Requires: zlib

%description
The Kmod package contains libraries and utilities for loading kernel modules

%package        devel
Summary:        Header and development files for kmod
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1

%build
autoreconf -vfi
%configure \
    --disable-manpages \
    --with-xz \
    --with-zlib \
    --with-openssl \
    --disable-silent-rules

%make_build

%install
%make_install pkgconfigdir=%{_libdir}/pkgconfig %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/bash-completion/completions/insmod
%{_datadir}/bash-completion/completions/lsmod
%{_datadir}/bash-completion/completions/rmmod
%exclude %{_datadir}/fish
%exclude %{_datadir}/zsh

%files devel
%defattr(-,root,root)
%{_datadir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Mon Mar 10 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 34.1-1
- Build with openssl
- This version fixes problem while fetching hash algo
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 30-6
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 30-5
- Release bump for SRP compliance
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 30-4
- Bump version as a part of zlib upgrade
* Mon Mar 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 30-3
- Add support to print signature info when ssl libs are present
* Fri Dec 23 2022 Oliver Kurth <okurth@vmware.com> 30-2
- bump version as part of xz upgrade
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 30-1
- Automatic Version Bump
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 29-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 29-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 28-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 27-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 26-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 25-2
- Cross compilation support
* Wed Sep 12 2018 Ankit Jain <ankitja@vmware.com> 25-1
- Updated to version 25
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 24-3
- Add devel package.
* Tue Jun 06 2017 Chang Lee <changlee@vmware.com> 24-2
- Remove %check
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 24-1
- Updated to version 24
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 21-4
- GA - Bump release of all rpms
* Thu Apr 21 2016 Anish Swaminathan <anishs@vmware.com> 21-3
- Add patch for return code fix in error path
* Fri Mar 25 2016 Alexey Makhalov <amakhalov@vmware.com> 21-2
- /bin/lsmod -> /sbin/lsmod
* Wed Jan 13 2016 Xiaolin Li <xiaolinl@vmware.com> 21-1
- Updated to version 21
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 16-1
- Initial build. First version
