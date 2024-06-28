Summary:    Attr-2.5.1
Name:       attr
Version:    2.5.1
Release:    2%{?dist}
License:    GPLv2+
URL:        https://savannah.nongnu.org/projects/attr
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://download.savannah.gnu.org/releases/attr/%{name}-%{version}.tar.gz
%define sha512 %{name}=8b4c043d61f8f3e0cd098e701181069f51117b85fd6ba18bfe9af77d894ea671232377d4793ffc822e9259ceee6ac71d75732eb93b2830c6cb5d0d918ba2d21b

%description
The attr package contains utilities to administer the extended attributes on filesystem objects.

%package    devel
Summary:    Libraries and header files for attr
Requires:   %{name} = %{version}-%{release}

%description    devel
Static libraries and header files for the support library for attr.

%package    lang
Summary:    Additional language files for attr
Group:      System Environment/Security
Requires:   %{name} = %{version}-%{release}

%description    lang
These are the additional language files of attr.

%prep
%autosetup -p1

%build
%configure \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

install -vdm 755 %{buildroot}%{_sysconfdir}
chmod -v 755 %{buildroot}%{_libdir}/libattr.so
ln -fsv ../sys/xattr.h %{buildroot}%{_includedir}/%{name}/xattr.h

#the man pages are already installed by man-pages package
rm -fv %{buildroot}/%{_libdir}/*.la \
       %{buildroot}%{_mandir}/man5/attr.5*

%find_lang %{name}

%if 0%{?with_check}
%check
%make_build check
%endif

%files
%defattr(-,root,root)
%{_mandir}/man1/*
%{_bindir}/*
%{_libdir}/*.so.*
%config(noreplace) %{_sysconfdir}/xattr.conf

%files devel
%defattr(-,root,root)
%doc %{_docdir}/%{name}/*
%{_libdir}/*.so
%{_mandir}/man3/*
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/libattr.pc

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Mon Jul 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.5.1-2
- Fix spec issues
- Move *.so to devel package
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 2.5.1-1
- Automatic Version Bump
* Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 2.4.48-1
- Updated to version 2.4.48
* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 2.4.47-4
- Added -lang and -devel subpackages
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.47-3
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  2.4.47-2
- Remove man pages provided by man-pages
* Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.47-1
- Initial version
