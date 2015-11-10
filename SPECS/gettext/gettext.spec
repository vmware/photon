Summary:	Utilities for internationalization and localization
Name:		gettext
Version:	0.18.3.2
Release:	2%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/gettext
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.gz
%define sha1 gettext=a2dc46d788edb0078ab20da7bd194bdb6da2f0d9
%description
These allow programs to be compiled with NLS
(Native Language Support), enabling them to output
messages in the user's native language.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/usr/share/doc/gettext-%{version}/examples
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/gettext/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a
%{_datarootdir}/aclocal/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*/*
%changelog
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 0.18.3.2-2
-	Handled locale files with macro find_lang
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 0.18.3.2-1
-	Initial build. First version
