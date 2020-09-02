%define perl_vendorarchdir %(test %{_host} == %{_build} && echo %{perl_vendorarch} || echo %{perl_vendorarch} | sed 's/x86_64-linux-thread-multi/%{_arch}-linux/')

Summary:        SQLite DBI Driver
Name:           perl-DBD-SQLite
Version:        1.66
Release:        1%{?dist}
Group:          Development/Libraries
License:        (GPL+ or Artistic) and Public Domain
URL:            http://search.cpan.org/dist/DBD-SQLite/
Source0:        https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/DBD-SQLite-%{version}.tar.gz
%define sha1    DBD-SQLite=524dc89cc330ee7372fe04de4a6048881cc543e4
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
%setup -q -n DBD-SQLite-%{version}
%patch0 -p1
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
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
     -name '*.bs' -size 0 \) -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%{perl_vendorarchdir}/auto/*
%{perl_vendorarchdir}/DBD/
%{_mandir}/man3/*

%changelog
*   Wed Sep 23 2020 Piyush Gupta <gpiyush@vmware.com> 1.66-1
-   Upgrade to version 1.66.
*   Thu May 14 2020 Ankit Jain <ankitja@vmware.com> 1.64-1
-   Updated to 1.64, Use system sqlite instead of bundled one
*   Wed Jul 03 2019 Alexey Makhalov <amakhalov@vmware.com> 1.62-2
-   Cross compilation support
*   Tue Jan 22 2019 Michelle Wang <michellew@vmware.com> 1.62-1
-   Update to version 1.62.
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.58-1
-   Update to version 1.58.
*   Tue Feb 20 2018 Xiaolin Li <xiaolinl@vmware.com> 1.54-2
-   Build perl-DBD-SQLite with sqlite-autoconf-3.22.0.
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 1.54-1
-   Upgraded to 1.54.
*   Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 1.50-3
-   Use sqlite-devel as a BuildRequires.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.50-2
-   GA - Bump release of all rpms.
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.50-1
-   Upgraded to version 1.50.
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.48-1
-   Upgrade version.
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.46-1
-   Initial version.
