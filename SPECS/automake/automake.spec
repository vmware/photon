Summary:    Programs for generating Makefiles
Name:       automake
Version:    1.16.5
Release:    3%{?dist}
URL:        http://www.gnu.org/software/automake
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/gnu/automake/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  autoconf

BuildArch:      noarch

%description
Contains programs for generating Makefiles for use with Autoconf.

%prep
%autosetup -p1

%build
sed -i 's:/\\\${:/\\\$\\{:' bin/automake.in
%configure \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%check
sed -i "s:./configure:LEXLIB=/usr/lib/libfl.a &:" t/lex-{clean,depend}-cxx.sh
sed -i "s|test ! -s stderr||g" t/distcheck-no-prefix-or-srcdir-override.sh
sed -i '53d' t/nobase-python.sh
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datarootdir}/aclocal/README
%{_datarootdir}/%{name}-1.16/*
%{_datarootdir}/aclocal-1.16/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*

%changelog
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.16.5-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.16.5-2
- Release bump for SRP compliance
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.16.5-1
- Upgrade to v1.16.5
* Sun Nov 15 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.16.1-2
- Added patch,Fix make check failure in python tests
* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 1.16.1-1
- Update version to 1.16.1
* Tue Jan 02 2018 Alexey Makhalov <amakhalov@vmware.com> 1.15.1-1
- Version update
* Fri Aug 04 2017 Danut Moraru <dmoraru@vmware.com> 1.15-4
- Disable check that fails test case
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.15-3
- Fix arch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.15-2
- GA - Bump release of all rpms
* Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 1.15-1
- Updated to version 1.15
* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.14.1-2
- Adding autoconf package to build time requires packages
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.14.1-1
- Initial build. First version
