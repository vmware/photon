Summary:	Attr-2.4.47
Name:		attr
Version:	2.4.47
Release:	3%{?dist}
License:	GPLv2+
URL:		https://www.gnu.org/software/hurd/community/gsoc/project_ideas/libcap.html
Source0:	http://download.savannah.gnu.org/releases/attr/%{name}-%{version}.src.tar.gz
%define sha1 attr=5060f0062baee6439f41a433325b8b3671f8d2d8
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
%description
The attr package contains utilities to administer the extended attributes on filesystem objects.
%prep
%setup -q
%build
sed -i -e 's|/@pkg_name@|&-@pkg_version@|' include/builddefs.in
INSTALL_USER=root  \
INSTALL_GROUP=root \
./configure --prefix=%{_prefix} --disable-static
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install install-dev install-lib
install -vdm 755 %{buildroot}/lib
chmod -v 755 %{buildroot}/usr/lib/libattr.so
mv -v %{buildroot}/usr/lib/libattr.so.* %{buildroot}/lib
#ln -sfv ../..%{_lib}/$(readlink %{buildroot}%{_lib}/libattr.so.1 ) %{buildroot}%{_libdir}/libattr.so
ln -sfv ../../lib/libattr.so.1 %{buildroot}/usr/lib/libattr.so
rm %{buildroot}/%{_libdir}/*.la

#the man pages are already installed by man-pages package
rm -rv %{buildroot}/%{_mandir}/man2
rm -fv %{buildroot}%{_mandir}/man5/attr.5*
rmdir "%{buildroot}%{_mandir}/man5"
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_libdir}/*.so
%{_bindir}/*
/lib/*.so.*
%{_includedir}/attr/*
%{_datadir}/locale/*
%{_docdir}/%{name}-%{version}/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.47-3
-	GA - Bump release of all rpms
* 	Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  2.4.47-2
- 	Remove man pages provided by man-pages
*	Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.47-1
-	Initial version
