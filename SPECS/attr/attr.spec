Summary:    Attr-2.4.48
Name:       attr
Version:    2.4.48
Release:    2%{?dist}
License:    GPLv2+
URL:        https://savannah.nongnu.org/projects/attr
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://download.savannah.gnu.org/releases/attr/%{name}-%{version}.tar.gz
%define sha512 %{name}=75f870a0e6e19b8975f3fdceee786fbaff3eadaa9ab9af01996ffa8e50fe5b2bba6e4c22c44a6722d11b55feb9e89895d0151d6811c1d2b475ef4ed145f0c923

%description
The attr package contains utilities to administer the extended attributes on filesystem objects.

%package devel
Summary:    Libraries and header files for attr
Requires:   %{name} = %{version}-%{release}

%description devel
Static libraries and header files for the support library for attr

%package lang
Summary: Additional language files for attr
Group:      System Environment/Security
Requires: %{name} = %{version}-%{release}

%description lang
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
* Thu Jul 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.4.48-2
- Fix spec issues
- mOve *.so to devel package
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
