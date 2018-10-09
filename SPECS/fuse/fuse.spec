Summary:        File System in Userspace (FUSE) utilities
Name:           fuse
Version:        2.9.7
Release:        4%{?dist}
License:        GPL+
URL:            http://fuse.sourceforge.net/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/libfuse/libfuse/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha1 fuse=cd174e3d37995a42fad32fac92f76cd18e24174f
Patch0:        fuse-types.patch

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program.

%package        devel
Summary:        Header and development files
Group:          Development/Libraries
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create fuse applications.

%prep
%setup -q
%ifarch aarch64
%patch0 -p1
%endif
%build
%configure --disable-static INIT_D_PATH=/tmp/init.d &&
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
make install \
    DESTDIR=%{buildroot}

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
*   Mon Oct 8 2018 Sriram Nambakam <snambakam@vmware.com> 2.9.7-4
-   Use %configure and set DESTDIR
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.9.7-3
-   Aarch64 support
*   Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.7-2
-   Move pkgconfig folder to devel package.
*   Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 2.9.7-1
-   Update to 2.9.7
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.5-2
-   GA - Bump release of all rpms
*   Tue Jan 26 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.5-1
-   Updated to version 2.9.5
*   Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 2.9.4-2
-   post/pre actions are removed.
*   Tue Jun 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.4-1
-   Initial version.

