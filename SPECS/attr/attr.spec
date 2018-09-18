Summary:	Attr-2.4.48
Name:		attr
Version:	2.4.48
Release:	1%{?dist}
License:	GPLv2+
URL:		https://www.gnu.org/software/hurd/community/gsoc/project_ideas/libcap.html
Source0:	http://download.savannah.gnu.org/releases/attr/%{name}-%{version}.tar.gz
%define sha1 %{name}=d7c88cb5db51c5e255a511b0a15e832fcdda5b4f
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
%description
The attr package contains utilities to administer the extended attributes on filesystem objects.

%package devel
Summary:	Libraries and header files for attr
Requires:	%{name} = %{version}-%{release}
%description devel
Static libraries and header files for the support library for attr

%package lang
Summary: Additional language files for attr
Group:		System Environment/Security
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of attr.

%prep
%setup -q
%build
./configure --prefix=%{_prefix} --disable-static
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/lib
chmod -v 755 %{buildroot}/usr/lib/libattr.so
mv -v %{buildroot}/usr/lib/libattr.so.* %{buildroot}/lib
#ln -sfv ../..%{_lib}/$(readlink %{buildroot}%{_lib}/libattr.so.1 ) %{buildroot}%{_libdir}/libattr.so
ln -sfv ../../lib/libattr.so.1 %{buildroot}/usr/lib/libattr.so

ln -sfv /usr/include/sys/xattr.h %{buildroot}%{_includedir}/%{name}/xattr.h

rm %{buildroot}/%{_libdir}/*.la

#the man pages are already installed by man-pages package
rm -fv %{buildroot}%{_mandir}/man5/attr.5*
%find_lang %{name}

%check
make  %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_mandir}/man1/*
%{_libdir}/*.so
%{_bindir}/*
/lib/*.so.*
%{_libdir}/pkgconfig/libattr.pc
%config(noreplace) %{_prefix}%{_sysconfdir}/xattr.conf

%files devel
%defattr(-,root,root)
%doc %{_docdir}/%{name}/*
%{_mandir}/man3/*
%{_includedir}/%{name}/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 2.4.48-1
-   Updated to version 2.4.48
*   Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 2.4.47-4
-   Added -lang and -devel subpackages
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.47-3
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  2.4.47-2
-   Remove man pages provided by man-pages
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.47-1
-   Initial version
