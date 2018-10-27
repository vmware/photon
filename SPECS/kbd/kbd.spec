Summary:	Key table files, console fonts, and keyboard utilities
Name:		kbd
Version:	2.0.4
Release:	2%{?dist}
License:	GPLv2
URL:		http://ftp.altlinux.org/pub/people/legion/kbd
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.altlinux.org/pub/people/legion/kbd/%{name}-%{version}.tar.xz
%define sha1 kbd=cf5d45c62d6af70b8b1f210d89193b52f5efb05d
Patch0:		kbd-2.0.4-backspace-1.patch
BuildRequires:	check >= 0.9.4
%description
The Kbd package contains key-table files, console fonts, and keyboard utilities.
%prep
%setup -q
%patch0 -p1
sed -i 's/\(RESIZECONS_PROGS=\)yes/\1no/g' configure
sed -i 's/resizecons.8 //'  docs/man/man8/Makefile.in
%build
CONFIG_CACHE=
DISABLE_TESTS=
if [ %{_host} != %{_build} ]; then
cat > config.cache << EOF
ac_cv_func_setpgrp_void=yes
ac_cv_func_malloc_0_nonnull=yes
ac_cv_func_realloc_0_nonnull=yes
EOF
CONFIG_CACHE=--cache-file=config.cache
DISABLE_TESTS=--disable-tests
fi
PKG_CONFIG_PATH=/tools/lib/pkgconfig \
%configure \
    --target=%{_target} \
	--disable-vlock \
	--disable-silent-rules \
    $CONFIG_CACHE \
    $DISABLE_TESTS
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -R -v docs/doc/* %{buildroot}%{_defaultdocdir}/%{name}-%{version}
rm -f %{buildroot}%{_defaultdocdir}/%{name}-%{version}/kbd.FAQ*
%find_lang %{name}

%check
make %{?_smp_mflags} check

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
*   Mon Sep 11 2017 Anish Swaminathan <anishs@vmware.com> 2.0.4-2
-   Remove FAQs from main package
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.4-1
-   Updated to version 2.0.4
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.3-2
-   GA - Bump release of all rpms
*   Wed Jan 13 2016 Xiaolin Li <xiaolinl@vmware.com> 2.0.3-1
-   Updated to version 2.0.3
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.0.1-1
-   Initial build. First version
