Summary:	The package automatically configure source code
Name:		autoconf
Version:	2.69
Release:	1
License:	GPLv2
URL:		http://www.gnu.org/software/autoconf
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/autoconf/%{name}-%{version}.tar.xz
%description
The package contains programs for producing shell scripts that can
automatically configure source code.
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
%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%{_datarootdir}/autoconf/*
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.69-1
-	Initial build.	First version
