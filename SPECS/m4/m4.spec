Summary:	A macro processor
Name:		m4
Version:	1.4.17
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/m4
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/m4/%{name}-%{version}.tar.xz
%define sha1 m4=74ad71fa100ec8c13bc715082757eb9ab1e4bbb0
%description
The M4 package contains a macro processor
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%check
sed -i -e '41s/ENOENT/& || errno == EINVAL/' tests/test-readlink.h
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	1.4.17-2
-	GA - Bump release of all rpms
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.4.17-1
-	Initial build.	First version
