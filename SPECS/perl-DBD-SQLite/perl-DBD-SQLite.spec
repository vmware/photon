%define perl_vendorarchdir %(test %{_host} == %{_build} && echo %{perl_vendorarch} || echo %{perl_vendorarch} | sed 's/x86_64-linux-thread-multi/%{_arch}-linux/')

Summary:        SQLite DBI Driver
Name:           perl-DBD-SQLite
Version:        1.72
Release:        4%{?dist}
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/DBD-SQLite/
Source0:        https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/DBD-SQLite-%{version}.tar.gz
%define sha512  DBD-SQLite=67a90c618a3626b3ae0b333b5eb4d4d0c8c13712bbcd50c135bf74e83dc252301664089803597c1bcbebf7f1eda040673d4438e70e2dae0aef3b8ebeeecd2f79

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
Patch0:         use-system-sqlite.patch
BuildRequires:  sqlite-devel
BuildRequires:  perl
BuildRequires:  perl-DBI
Requires:       perl-DBI
Requires:       perl
Requires:       sqlite-libs

%description
SQLite is a public domain RDBMS database engine that you can find at
http://www.hwaci.com/sw/sqlite/.

This module provides a SQLite RDBMS module that uses the system SQLite
libraries.

%prep
%autosetup -n DBD-SQLite-%{version}
rm sqlite*

%build
CFLAGS="%{optflags}" perl Makefile.PL INSTALLDIRS=vendor AR=%{_host}-ar CC=%{_host}-gcc LD=%{_host}-gcc OPTIMIZE="%{optflags}"
if [ %{_host} != %{_build} ]; then
ln -s /target-%{_arch}%{perl_privlib}/%{_arch}-linux %{perl_privlib}/%{_arch}-linux
ln -s /target-%{_arch}%{perl_vendorlib}/%{_arch}-linux %{perl_vendorlib}/%{_arch}-linux
sed -i 's/x86_64-linux-thread-multi/%{_arch}-linux/' Makefile
fi
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
     -name '*.bs' -size 0 \) -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} test

%files
%{perl_vendorarchdir}/auto/*
%{perl_vendorarchdir}/DBD/
%{_mandir}/man3/*

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.72-4
- Release bump for SRP compliance
* Fri Feb 23 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.72-3
- Bump version as a part of sqlite upgrade to v3.43.2
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 1.72-2
- bump release as part of sqlite update
* Thu Dec 08 2022 Gerrit Photon <photon-checkins@vmware.com> 1.72-1
- Automatic Version Bump
* Wed Sep 23 2020 Piyush Gupta <gpiyush@vmware.com> 1.66-1
- Upgrade to version 1.66.
* Thu May 14 2020 Ankit Jain <ankitja@vmware.com> 1.64-1
- Updated to 1.64, Use system sqlite instead of bundled one
* Wed Jul 03 2019 Alexey Makhalov <amakhalov@vmware.com> 1.62-2
- Cross compilation support
* Tue Jan 22 2019 Michelle Wang <michellew@vmware.com> 1.62-1
- Update to version 1.62.
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.58-1
- Update to version 1.58.
* Tue Feb 20 2018 Xiaolin Li <xiaolinl@vmware.com> 1.54-2
- Build perl-DBD-SQLite with sqlite-autoconf-3.22.0.
* Mon Apr 3 2017 Robert Qi <qij@vmware.com> 1.54-1
- Upgraded to 1.54.
* Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 1.50-3
- Use sqlite-devel as a BuildRequires.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.50-2
- GA - Bump release of all rpms.
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.50-1
- Upgraded to version 1.50.
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.48-1
- Upgrade version.
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.46-1
- Initial version.
