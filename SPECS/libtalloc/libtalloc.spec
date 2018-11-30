Summary:    Talloc is a hierarchical, reference counted memory pool system
Name:       libtalloc
Version:    2.1.14
Release:    2%{?dist}
License:    LGPLv3+
URL:        https://talloc.samba.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
%define sha1 talloc=9d563b768148b620bdae1c97b36cfc30928a1044
BuildRequires: libxslt
BuildRequires: docbook-xsl
BuildRequires: python2-devel

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

%build
%configure --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules
make %{?_smp_mflags} V=1

%install
%make_install
rm -f %{buildroot}/usr/share/swig/*/talloc.i

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libtalloc.so.*

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
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.1.14-2
-   Added BuildRequires python2-devel
*   Tue Sep 11 2018 Bo Gan <ganb@vmware.com> 2.1.14-1
-   Update to 2.1.14
*   Thu Aug 03 2017 Chang Lee <changlee@vmware.com> 2.1.9-2
-   Copy libraries and add a patch for path regarding %check
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 2.1.9-1
-   Initial packaging
