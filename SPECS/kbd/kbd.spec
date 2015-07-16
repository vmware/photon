Summary:	Key table files, console fonts, and keyboard utilities
Name:		kbd
Version:	2.0.1
Release:	1%{?dist}
License:	GPLv2
URL:		http://ftp.altlinux.org/pub/people/legion/kbd
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.altlinux.org/pub/people/legion/kbd/%{name}-%{version}.tar.gz
%define sha1 kbd=8d7d6f9fc95d8abb80156da0713a4cbc0dbfda97
Patch0:		kbd-2.0.1-backspace-1.patch
BuildRequires:	check >= 0.9.4
%description
The Kbd package contains key-table files, console fonts, and keyboard utilities.
%prep
%setup -q
%patch0 -p1
sed -i 's/\(RESIZECONS_PROGS=\)yes/\1no/g' configure
sed -i 's/resizecons.8 //'  docs/man/man8/Makefile.in
%build
PKG_CONFIG_PATH=/tools/lib/pkgconfig \
./configure \
	--prefix=%{_prefix} \
	--disable-vlock \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -R -v docs/doc/* %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/consolefonts/*
%{_datarootdir}/consoletrans/*
%{_datarootdir}/keymaps/*
%{_datarootdir}/unimaps/*
%{_mandir}/*/*
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.0.1-1
-	Initial build. First version
