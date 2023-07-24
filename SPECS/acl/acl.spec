Summary:        Access control list utilities
Name:           acl
Version:        2.3.1
Release:        2%{?dist}
License:        GPLv2+
Group:          System Environment/Base
URL:            https://savannah.nongnu.org/projects/%{name}
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz
%define sha512 %{name}=f101e27058c959f4c412f475c3fc77a90d1ead8728701e4ce04ff08b34139d35e0e72278c9ac7622ba6054e81c0aeca066e09491b5f5666462e3866705a0e892

Requires:       libacl = %{version}-%{release}

BuildRequires:  attr-devel

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n libacl
Summary:    Dynamic library for access control list support
License:    LGPLv2+
Group:      System Environment/Libraries
Requires:   attr

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary:    Files needed for building programs with libacl
License:    LGPLv2+
Group:      Development/Libraries
Requires:   libacl = %{version}-%{release}
Requires:   attr-devel

%description -n libacl-devel
This package contains header files and documentation needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%autosetup -p1

%build
%configure \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%find_lang %{name}

%check
if ./setfacl -m u:$(id -u):rwx .; then
  %make_build check
else
  echo '*** The chroot file system does not support all ACL options ***'
fi

%post -n libacl
/sbin/ldconfig

%postun -n libacl
/sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man5/acl.5*

%files -n libacl-devel
%defattr(-,root,root)
%{_libdir}/libacl.so
%{_includedir}/%{name}
%{_includedir}/sys/acl.h
%{_mandir}/man3/acl_*
%{_docdir}/acl/*
%{_libdir}/pkgconfig/libacl.pc

%files -n libacl
%defattr(-,root,root)
%{_libdir}/libacl.so.*

%changelog
* Mon Jul 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.3.1-2
- Fix spec issues
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 2.3.1-1
- Automatic Version Bump
* Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 2.2.53-1
- Updated to version 2.2.53
* Fri Jul 28 2017 Chang Lee <changlee@vmware.com> 2.2.52-5
- Fixed %check for filtering unsupported check env
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.2.52-4
- BuildRequired attr-devel.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.2.52-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.52-2
- GA - Bump release of all rpms
* Thu Feb 26 2015 Divya Thaluru <dthaluru@vmware.com> 2.2.52-1
- Initial version
