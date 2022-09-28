Summary:        Talloc is a hierarchical, reference counted memory pool system
Name:           libtalloc
Version:        2.3.4
Release:        1%{?dist}
License:        LGPLv3+
URL:            https://talloc.samba.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:    https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
%define sha512  talloc=c46488deda99753fd79566d42cae88899b71196513a127813be2cb855e7f36b77132f0552297ee4153ba4d8f177cea3bb0dc93340caabf321c026657744684d9

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
Provides: python-talloc = %{version}-%{release}
Obsoletes: python-talloc < 2.3.4-1

%description -n python3-talloc
Python 3 libraries for creating bindings using talloc

%package -n python3-talloc-devel
Group: Development/Libraries
Summary: Development libraries for python-talloc
Requires: python3-talloc = %{version}-%{release}
Provides: python-talloc-devel = %{version}-%{release}
Obsoletes: python-talloc-devel < 2.3.4-1

%description -n python3-talloc-devel
Development libraries for python-talloc

%prep
%autosetup -p1 -n talloc-%{version}

%build
%configure --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules \
           --enable-debug

%make_build

%install
%make_install %{?_smp_mflags}
rm -f %{buildroot}/usr/share/swig/*/talloc.i

%if 0%{?with_check}
%check
%make_build check
%endif

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
%{python3_sitelib}/*
%{_libdir}/libpytalloc-util.cpython*.so.*

%files -n python3-talloc-devel
%defattr(-,root,root)
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.cpython-*.pc
%{_libdir}/libpytalloc-util.cpython*.so

%changelog
*   Thu Sep 22 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 2.3.4-1
-   Version increase needed for SSSD addition. Forces update to python 3 packages.
-   Enable debuginfo.
*   Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.1.14-3
-   Bump version as a part of libxslt upgrade
*   Mon Jan 06 2020 Prashant S Chauhan <psinghchauha@vmware.com> 2.1.14-2
-   Added python2-devel as a build requirement
*   Tue Sep 11 2018 Bo Gan <ganb@vmware.com> 2.1.14-1
-   Update to 2.1.14
*   Thu Aug 03 2017 Chang Lee <changlee@vmware.com> 2.1.9-2
-   Copy libraries and add a patch for path regarding %check
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 2.1.9-1
-   Initial packaging
