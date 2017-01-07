Summary:    Utilities for managing the XFS filesystem
Name:       xfsprogs
Version:    4.9.0
Release:    1%{?dist}
License:    GPL+ and LGPLv2+
URL:        http://oss.sgi.com/projects/xfs/
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    http://kernel.org/pub/linux/utils/fs/xfs/xfsprogs/%{name}-%{version}.tar.gz
%define sha1 xfsprogs=6d6dcf7f0bbf0e0104fb47af0cba1647817cf6e8
BuildRequires:  gettext
BuildRequires:  readline-devel
%description
The xfsprogs package contains administration and debugging tools for the
XFS file system. A set of commands to use the XFS filesystem, including
mkfs.xfs.

XFS is a high performance journaling filesystem which originated
on the SGI IRIX platform.It is completely multi-threaded, can
support large files and large filesystems, extended attributes,
variable block sizes, is extent based, and makes extensive use of
Btrees (directories, extents, free space) to aid both performance
and scalability.

%package devel
Summary: XFS filesystem-specific static libraries and headers
Group: Development/Libraries
Requires: xfsprogs = %{version}-%{release}

%description devel
xfsprogs-devel contains the libraries and header files needed to
develop XFS filesystem-specific programs.

%prep
%setup -q

%build
./configure \
    --enable-readline=yes \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir}

make INSTALL_USER=root INSTALL_GROUP=root %{?_smp_mflags}

%install
make  DIST_ROOT=$RPM_BUILD_ROOT PKG_DOC_DIR=%{_usr}/share/doc/%{name}-%{version} \
PKG_ROOT_SBIN_DIR=%{_sbindir} PKG_ROOT_LIB_DIR=%{_libdir} install install-dev

rm -f $RPM_BUILD_ROOT/{%{_lib}/*.{la,a,so},%{_libdir}/*.{la,a}}
find %{buildroot}/%{_lib64dir} -name '*.la' -delete
find %{buildroot}/%{_lib64dir} -name '*.a' -delete
chmod 0755 $RPM_BUILD_ROOT/%{_libdir}/libhandle.so.*

rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/xfsprogs/
%find_lang %{name}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/CHANGES doc/COPYING doc/CREDITS README
%{_libdir}/*.so.*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_mandir}/man3/*
%dir %{_includedir}/xfs
%{_includedir}/xfs/*

%changelog
*   Fri Jan 6 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.0-1
-   Initial build.  First version
