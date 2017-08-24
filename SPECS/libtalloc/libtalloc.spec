Summary:    Talloc is a hierarchical, reference counted memory pool system
Name:       libtalloc
Version:    2.1.9
Release:    2%{?dist}
License:    LGPLv3+
URL:        https://talloc.samba.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://www.samba.org/ftp/talloc/talloc-2.1.9.tar.gz
%define sha1 talloc=e1e79fec4c0b6bd92be904a9c03b0a168478711a
Patch0:      wscript-test_magic_differs.patch
BuildRequires: libxslt
BuildRequires: docbook-xsl

%description
Libtalloc alloc is a hierarchical, reference counted memory pool system with destructors. It is the core memory allocator used in Samba.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libtalloc-devel package contains libraries and header files for libtalloc

%package -n python-talloc
Group: Development/Libraries
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}

%description -n python-talloc
Python 2 libraries for creating bindings using talloc

%package -n python-talloc-devel
Group: Development/Libraries
Summary: Development libraries for python-talloc
Requires: python-talloc = %{version}-%{release}

%description -n python-talloc-devel
Development libraries for python-talloc

%prep
%setup -q -n talloc-%{version}
%patch0 -p1

%build
%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules
make %{?_smp_mflags} V=1

%install
%make_install
find %{buildroot}  -name "*.so*" -exec chmod -c +x {} \;
rm -f %{buildroot}/%{_libdir}/libtalloc.a
rm -f %{buildroot}/usr/share/swig/*/talloc.i

%check
cp %{buildroot}/usr/lib/libtalloc.so.2 /usr/lib/
cp %{buildroot}/usr/lib/libpytalloc-util.so.2 /usr/lib/
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so.*

%files devel
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3.gz

%files -n python-talloc
%{_libdir}/libpytalloc-util.so.*
%{_libdir}/python2.7/site-packages/*

%files -n python-talloc-devel
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.pc
%{_libdir}/libpytalloc-util.so

%changelog
*   Thu Aug 03 2017 Chang Lee <changlee@vmware.com> 2.1.9-2
-   Copy libraries and add a patch for path regarding %check
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 2.1.9-1
-   Initial packaging
