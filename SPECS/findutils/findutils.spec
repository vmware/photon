Summary:	This package contains programs to find files
Name:		findutils
Version:	4.4.2
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/findutils
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/findutils/%{name}-%{version}.tar.gz
%define sha1 findutils=e8dd88fa2cc58abffd0bfc1eddab9020231bb024
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
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
/bin/find
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/*/*
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.4.2-1
-	Initial build.	First version
