Summary:        Simple package manager built on top of hawkey and librepo
Name:           libhif
Version:        0.2.3
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/hughsie/libhif
Source0:        http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
%define sha1    libhif=b5cec26e848e2fb1caf36ec9fcd4c9019e86b566
Patch0:         libhif-makecheck.patch
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  glib-devel >= 2.16.1
BuildRequires:  libtool
BuildRequires:  gtk-doc
BuildRequires:  gobject-introspection-devel
BuildRequires:  hawkey-devel >= 0.4.6
BuildRequires:  rpm-devel >= 4.11.0
BuildRequires:  librepo-devel >= 1.7.11
BuildRequires:  libsolv-devel
BuildRequires:  popt-devel
BuildRequires:  python2-libs
BuildRequires:  python2
BuildRequires:  gobject-introspection-python
BuildRequires:  openssl-devel

Requires:       openssl
Requires:       librepo
Requires:       libsolv
Requires:       gobject-introspection
Requires:       hawkey
Requires:       rpm-libs
Requires:       glib >= 2.16.1

%description
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package devel
Summary: GLib Libraries and headers for libhif
Requires: libhif
Provides: pkgconfig(libhif)

%description devel
GLib headers and libraries for libhif.

%prep
%setup -q
%patch0 -p1
%build

./autogen.sh --prefix=/usr \
    LDFLAGS='-L/usr/lib -lrpm -lrepo' \
        --enable-gtk-doc \
        --disable-static \
        --disable-silent-rules \
        --disable-dependency-tracking \

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libhif*.la

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.md AUTHORS NEWS COPYING
%{_libdir}/libhif.so.1*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_libdir}/libhif.so
%{_libdir}/pkgconfig/libhif.pc
%dir %{_includedir}/libhif
%{_includedir}/libhif/*.h
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/*.gir

%changelog
*   Sat Aug 19 2017 Chang Lee <changlee@vmware.com> 0.2.3-1
-   Updated to 0.2.3
-   Disabled GLib-GObject-CRITICAL tests due to Segmentation fault in all tests
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 0.2.2-5
-   BuildRequires libsolv-devel.
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 0.2.2-4
-   Use rpm-libs at runtime
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 0.2.2-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.2.2-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 0.2.2-1
-   Updated to new version.
*   Wed Jun 17 2015 Anish Swaminathan <anishs@vmware.com> 0.2.0-1
-   Updated version