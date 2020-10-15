Summary:    Talloc is a hierarchical, reference counted memory pool system
Name:       libtalloc
Version:    2.3.1
Release:    4%{?dist}
License:    LGPLv3+
URL:        https://talloc.samba.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
%define sha1 talloc=1ff430a62264b29efac39a3fa26290586c019800
BuildRequires: libxslt
BuildRequires: docbook-xsl
BuildRequires: python3-devel
BuildRequires: which

%description
Libtalloc alloc is a hierarchical, reference counted memory pool system with destructors. It is the core memory allocator used in Samba.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libtalloc-devel package contains libraries and header files for libtalloc

%package -n python3-talloc
Group: Development/Libraries
Summary: Python bindings for the Talloc library
Requires: libtalloc = %{version}-%{release}
Requires: python3
%description -n python3-talloc
Python 2 libraries for creating bindings using talloc

%package -n python3-talloc-devel
Group: Development/Libraries
Summary: Development libraries for python-talloc
Requires: python3-talloc = %{version}-%{release}

%description -n python3-talloc-devel
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
%defattr(-,root,root)
%{_libdir}/libtalloc.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3.gz

%files -n python3-talloc
%defattr(-,root,root)
%{_libdir}/python3.9/site-packages/*
%ifarch x86_64
%{_libdir}/libpytalloc-util.cpython-39-x86-64-linux-gnu.so.2
%{_libdir}/libpytalloc-util.cpython-39-x86-64-linux-gnu.so.2.3.1
%endif
%ifarch aarch64
%{_libdir}/libpytalloc-util.cpython-39-aarch64-linux-gnu.so.2
%{_libdir}/libpytalloc-util.cpython-39-aarch64-linux-gnu.so.2.3.1
%endif

%files -n python3-talloc-devel
%defattr(-,root,root)
%{_includedir}/pytalloc.h
%ifarch x86_64
%{_libdir}/libpytalloc-util.cpython-39-x86-64-linux-gnu.so
%{_libdir}/pkgconfig/pytalloc-util.cpython-39-x86_64-linux-gnu.pc
%endif
%ifarch aarch64
%{_libdir}/libpytalloc-util.cpython-39-aarch64-linux-gnu.so
%{_libdir}/pkgconfig/pytalloc-util.cpython-39-aarch64-linux-gnu.pc
%endif

%changelog
*   Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 2.3.1-4
-   Build with python 3.9
*   Wed Jul 29 2020 Tapas Kundu <tkundu@vmware.com> 2.3.1-3
-   Build with python3
*   Fri Jul 24 2020 Tapas Kundu <tkundu@vmware.com> 2.3.1-2
-   Added pkg files for aarch64 and x86.
*   Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 2.3.1-1
-   Update to 2.3.1
-   Mass removal python2 and build with python3
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.1.14-2
-   Added BuildRequires python2-devel
*   Tue Sep 11 2018 Bo Gan <ganb@vmware.com> 2.1.14-1
-   Update to 2.1.14
*   Thu Aug 03 2017 Chang Lee <changlee@vmware.com> 2.1.9-2
-   Copy libraries and add a patch for path regarding %check
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 2.1.9-1
-   Initial packaging
