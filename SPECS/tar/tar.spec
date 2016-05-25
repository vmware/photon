Summary:	Archiving program
Name:		tar
Version:	1.28
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/tar
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	tar/%{name}-%{version}.tar.xz
%define sha1 tar=40f3470a96b80749531fe48dbba99e43b6dfa7d3
%description
Contains GNU archiving program
%prep
%setup -q
%build
FORCE_UNSAFE_CONFIGURE=1  ./configure \
	--prefix=%{_prefix} \
	--bindir=/bin \
	--disable-silent-rules
make %{?_smp_mflags}
%install
install -vdm 755 %{buildroot}%{_sbindir}
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} -C doc install-html docdir=%{_defaultdocdir}/%{name}-%{version}
install -vdm 755 %{buildroot}/usr/share/man/man1 
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files -f %{name}.lang
%defattr(-,root,root)
/bin/tar
%{_libexecdir}/rmt
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-2
-	GA - Bump release of all rpms
*	Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-1
-	Update to 1.28-1.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.27.1-1
-	Initial build.	First version
