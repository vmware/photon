Summary:        File System in Userspace (FUSE) utilities
Name:           fuse
Version:        2.9.9
Release:        4%{?dist}
URL:            http://fuse.sourceforge.net/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/libfuse/libfuse/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha512  fuse=1acd51a647ec3dbf9eaafb80cec92bd8542bcbb2cf4510fc8b079b4f8aaa8f4b301e469ddefe4f1cc4ae2bf941e028077601c20d97f187cc618cea8710cbe331

Source1: license.txt
%include %{SOURCE1}

%ifarch aarch64
Patch0:         fuse-types.patch
%endif
Patch1:         fuse-prevent-silent-truncation.patch
Patch2:         fuse2-0007-util-ulockmgr_server.c-conditionally-define-closefro.patch

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create fuse applications.

%prep
# Using autosetup is not feasible
%setup -qn libfuse-%{name}-%{version}
%ifarch aarch64
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1

%build
./makeconf.sh
%configure --disable-static INIT_D_PATH=/tmp/init.d &&
%make_build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
%make_install %{?_smp_mflags}
install -v -m755 -d /usr/share/doc/%{name}-%{version} &&
install -v -m644    doc/{how-fuse-works,kernel.txt} \
                    /usr/share/doc/%{name}-%{version}
find %{buildroot} -name '*.la' -delete

%files
%defattr(-, root, root)
/sbin/mount.fuse
%{_libdir}/libfuse.so.*
%{_libdir}/libulockmgr.so.*
%{_bindir}/*
%{_mandir}/man1/*
%exclude %{_mandir}/man8/*
%exclude /tmp/init.d/fuse
%exclude %{_sysconfdir}/udev/rules.d/99-fuse.rules

%files devel
%doc ChangeLog
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_includedir}/*
%{_libdir}/pkgconfig/fuse.pc

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.9.9-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.9.9-3
- Release bump for SRP compliance
* Mon Aug 22 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.9.9-2
- Fix build with glibc 2.36
* Wed Jul 15 2020 Gerrit Photon <photon-checkins@vmware.com> 2.9.9-1
- Automatic Version Bump
* Fri Jan 18 2019 Ankit Jain <ankitja@vmware.com> 2.9.7-5
- Added patches for CVE-2018-10906 and hardening changes
* Mon Oct 8 2018 Sriram Nambakam <snambakam@vmware.com> 2.9.7-4
- Use %configure and set DESTDIR
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.9.7-3
- Aarch64 support
* Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.7-2
- Move pkgconfig folder to devel package.
* Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 2.9.7-1
- Update to 2.9.7
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.5-2
- GA - Bump release of all rpms
* Tue Jan 26 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.5-1
- Updated to version 2.9.5
* Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 2.9.4-2
- post/pre actions are removed.
* Tue Jun 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.4-1
- Initial version.
