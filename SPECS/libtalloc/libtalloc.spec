Summary:    Talloc is a hierarchical, reference counted memory pool system
Name:       libtalloc
Version:    2.4.1
Release:    1%{?dist}
License:    LGPLv3+
URL:        https://talloc.samba.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
%define sha512 talloc=4de3b66d7cd1ff3f53e28e86bf9e89528635465c67868e1262aab6946106c228b2c184e988561361c3194fb260d83e016477254c9dbea7abff40c4dc0d31c76c

BuildRequires: libxslt-devel
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
Python 3 libraries for creating bindings using talloc

%package -n python3-talloc-devel
Group: Development/Libraries
Summary: Development libraries for python-talloc
Requires: python3-talloc = %{version}-%{release}

%description -n python3-talloc-devel
Development libraries for python-talloc

%prep
%autosetup -p1 -n talloc-%{version}

%build
%configure --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules

%make_build

%install
%make_install

%if 0%{?with_check}
%check
%make_build check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

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
%{_libdir}/libpytalloc*.cpython*.so.*

%files -n python3-talloc-devel
%defattr(-,root,root)
%{_includedir}/pytalloc.h
%{_libdir}/libpytalloc*.cpython*.so
%{_libdir}/pkgconfig/pytalloc*.cpython*.pc

%changelog
* Fri May 16 2025 Michelle Wang <michelle.wang@broadcom.com> 2.4.1-1
- Bump up version to 2.4.1 required by samba-client 4.19.3
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.4.0-1
- Version upgrade for SSSD.
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.3.1-5
- Update release to compile with python 3.10
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 2.3.1-4
- Build with python 3.9
* Wed Jul 29 2020 Tapas Kundu <tkundu@vmware.com> 2.3.1-3
- Build with python3
* Fri Jul 24 2020 Tapas Kundu <tkundu@vmware.com> 2.3.1-2
- Added pkg files for aarch64 and x86.
* Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 2.3.1-1
- Update to 2.3.1
- Mass removal python2 and build with python3
* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.1.14-2
- Added BuildRequires python2-devel
* Tue Sep 11 2018 Bo Gan <ganb@vmware.com> 2.1.14-1
- Update to 2.1.14
* Thu Aug 03 2017 Chang Lee <changlee@vmware.com> 2.1.9-2
- Copy libraries and add a patch for path regarding %check
* Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 2.1.9-1
- Initial packaging
