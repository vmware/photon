Summary:        Utilities for loading kernel modules
Name:           kmod
Version:        29
Release:        2%{?dist}
License:        LGPLv2.1+ and GPLv2+
URL:            http://www.kernel.org/pub/linux/utils/kernel/kmod
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
%define sha512  %{name}-%{version}=557cdcaec75e5a1ceea2d10862c944e9a65ef54f6ee9da6dc98ce4582418fdc9958aab2e14a84807db61daf36ec4fcdc23a36376c39d5dc31d1823ca7cd47998

BuildRequires:  xz-devel
BuildRequires:  zlib-devel

Requires:       xz

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
%configure \
    --with-rootlibdir=%{_lib} \
    --disable-manpages \
    --with-xz \
    --with-zlib \
    --disable-silent-rules

make VERBOSE=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} pkgconfigdir=%{_libdir}/pkgconfig install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_sbindir}
for target in depmod insmod lsmod modinfo modprobe rmmod; do
  ln -sv %{_bindir}/kmod %{buildroot}%{_sbindir}/$target
done
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_sbindir}/*
%{_datadir}/bash-completion/completions/kmod

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so

%changelog
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
