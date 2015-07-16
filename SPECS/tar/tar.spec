Summary:	Archiving program
Name:		tar
Version:	1.27.1
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/tar
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	tar/%{name}-%{version}.tar.xz
%define sha1 tar=5ce4233e1774e990b930f3c46990267b28448962
Patch0:		tar-1.27.1-manpage-1.patch
%description
Contains GNU archiving program
%prep
%setup -q
%patch0 -p1
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
perl tarman > %{buildroot}/usr/share/man/man1/tar.1
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
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.27.1-1
-	Initial build.	First version
