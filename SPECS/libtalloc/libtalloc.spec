Summary:    Talloc is a hierarchical, reference counted memory pool system
Name:       libtalloc
Version:    2.4.0
Release:    1%{?dist}
License:    LGPLv3+
URL:        https://talloc.samba.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
%define sha512 talloc=810d92a614d0b9e0ac6fe403c1643c4dda435f79c4627d3c3be228f94b4b2ee8e528efbbed07f7d1a16043d6e55bdf4f10826f31fb8ca1c649c4126ea09a3aff

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
Group:      Development/Libraries
Summary:    Python bindings for the Talloc library
Requires:   %{name} = %{version}-%{release}
Requires:   python3

%description -n python3-talloc
Python3 libraries for creating bindings using talloc

%package -n python3-talloc-devel
Group:      Development/Libraries
Summary:    Development libraries for python-talloc
Requires:   python3-talloc = %{version}-%{release}

%description -n python3-talloc-devel
Development libraries for python-talloc

%prep
%autosetup -p1 -n talloc-%{version}

%build
%configure \
    --bundled-libraries=NONE \
    --builtin-libraries=replace \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
rm -f %{buildroot}%{_datadir}/swig/*/talloc.i

%check
make check %{?_smp_mflags}

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
%{_libdir}/libpytalloc-util.cpython-311*linux-gnu.so.*
%{_libdir}/python%{python3_version}/site-packages/*

%files -n python3-talloc-devel
%defattr(-,root,root)
%{_includedir}/pytalloc.h
%{_libdir}/libpytalloc-util.cpython-311*linux-gnu.so
%{_libdir}/pkgconfig/pytalloc-util.cpython-311*linux-gnu.pc

%changelog
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.4.0-1
- Version bump for SSSD
* Sun Dec 11 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.3.4-2
- Fix build error on arm machine
* Tue Dec 06 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.3.4-1
- Update to version 2.3.4
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.3.3-4
- Update release to compile with python 3.11
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.3.3-3
- Bump version as a part of libxslt upgrade
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.3.3-2
- Bump version as a part of libxslt upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.3.3-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.3.2-1
- Automatic Version Bump
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
- Initial packaging.
