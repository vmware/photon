Summary:    Key table files, console fonts, and keyboard utilities
Name:       kbd
Version:    2.2.0
Release:    1%{?dist}
License:    GPLv2
URL:        http://ftp.altlinux.org/pub/people/legion/kbd
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.altlinux.org/pub/people/legion/kbd/%{name}-%{version}.tar.xz
%define sha512 %{name}=5f407c20739487e423e8390e429d30838a1a69a0a50db083803ce56da919e25ce480b63fd1bcfac9eb362095f17e575783b09eaa55e26b442bfa3ed838e04f13

Patch0:     kbd-2.0.4-backspace-1.patch

BuildRequires:  check-devel

Conflicts:      toybox < 0.8.2-2

%description
The Kbd package contains key-table files, console fonts, and keyboard utilities.

%prep
%autosetup -p1
sed -i 's/\(RESIZECONS_PROGS=\)yes/\1no/g' configure
sed -i 's/resizecons.8 //'  docs/man/man8/Makefile.in

%build
export PKG_CONFIG_PATH=/tools/lib/pkgconfig
%configure \
     --disable-vlock \
     --disable-silent-rules
%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_docdir}/%{name}-%{version}
cp -R -v docs/doc/* %{buildroot}%{_docdir}/%{name}-%{version}
rm -f %{buildroot}%{_docdir}/%{name}-%{version}/kbd.FAQ*
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/consolefonts/*
%{_datadir}/consoletrans/*
%{_datadir}/keymaps/*
%{_datadir}/unimaps/*
%{_docdir}/%{name}-%{version}/*
%{_mandir}/*/*

%changelog
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.2.0-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.0-1
- Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 2.0.4-4
- Do not conflict with toybox >= 0.8.2-2
* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 2.0.4-3
- Add conflict toybox.
* Mon Sep 11 2017 Anish Swaminathan <anishs@vmware.com> 2.0.4-2
- Remove FAQs from main package.
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.4-1
- Updated to version 2.0.4.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.3-2
- GA - Bump release of all rpms.
* Wed Jan 13 2016 Xiaolin Li <xiaolinl@vmware.com> 2.0.3-1
- Updated to version 2.0.3.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.0.1-1
- Initial build First version.
