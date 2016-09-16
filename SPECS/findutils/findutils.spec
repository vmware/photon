Summary:	This package contains programs to find files
Name:		findutils
Version:	4.6.0
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/findutils
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/findutils/%{name}-%{version}.tar.gz
%define sha1 findutils=f18e8aaee3f3d4173a1f598001003be8706d28b0
%description
These programs are provided to recursively search through a
directory tree and to create, maintain, and search a database
(often faster than the recursive find, but unreliable if the
database has not been recently updated).
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--localstatedir=%{_sharedstatedir}/locate \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/find %{buildroot}/bin
sed -i 's/find:=${BINDIR}/find:=\/bin/' %{buildroot}%{_bindir}/updatedb
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
/bin/find
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/*/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.6.0-2
-	GA - Bump release of all rpms
*   	Tue Apr 26 2016 Anish Swaminathan <anishs@vmware.com> 4.6.0-1
-   	Updated to version 4.6.0
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.4.2-1
-	Initial build.	First version
