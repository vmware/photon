Summary:        SQLite DBI Driver
Name:           perl-DBD-SQLite
Version:        1.66
Release:        2%{?dist}
Group:          Development/Libraries
License:        (GPL+ or Artistic) and Public Domain
URL:            http://search.cpan.org/dist/DBD-SQLite
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/DBD-SQLite-%{version}.tar.gz
%define sha512  DBD-SQLite=4d58003e69f29b18d01ed0b5853cdac40ec9ce5d4c75bc8a3743937897a38290a99be30b1b9fae593b0d8d51d05b7e2438d29f7a7c1c755b66de51826397aef9

Patch0:         use-system-sqlite.patch

BuildRequires:  sqlite-devel
BuildRequires:  perl
BuildRequires:  perl-DBI
BuildRequires:  sed

Requires:       perl-DBI
Requires:       perl
Requires:       sqlite-libs

%description
SQLite is a public domain RDBMS database engine that you can find at
http://www.hwaci.com/sw/sqlite/.

This module provides a SQLite RDBMS module that uses the system SQLite
libraries.

%prep
%autosetup -p1 -n DBD-SQLite-%{version}
rm sqlite*

%build
export CFLAGS="%{optflags}"
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1

if [ %{_host} != %{_build} ]; then
  ln -sfv /target-%{_arch}%{perl_privlib}/%{_arch}-linux %{perl_privlib}/%{_arch}-linux
  ln -sfv /target-%{_arch}%{perl_vendorlib}/%{_arch}-linux %{perl_vendorlib}/%{_arch}-linux
  sed -i 's/x86_64-linux-thread-multi/%{_arch}-linux/' Makefile
fi

%make_build OPTIMIZE="%{optflags}"

%install
%make_install
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
make test %{?_smp_mflags}
%endif

%files
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/DBD/
%{_mandir}/man3/*

%changelog
* Tue Jun 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.66-2
- Bump version as a part of sqlite upgrade
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
