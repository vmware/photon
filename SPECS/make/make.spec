Summary:	Program for compiling packages
Name:		make
Version:	4.0
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/make
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.bz2
%define sha1 make=c819622dc84e2290c351646b8a0ec4df0df12bb6
%description
The Make package contains a program for compiling packages.
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
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/gnumake.h
%{_mandir}/*/*
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.0-1
-	Initial build.	First version
