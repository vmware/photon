%define perl_vendorarchdir %(test %{_host} == %{_build} && echo %{perl_vendorarch} || echo %{perl_vendorarch} | sed 's/x86_64-linux-thread-multi/%{_arch}-linux/')

# Got the intial spec from Fedora and modified it
Summary:        SQLite DBI Driver
Name:           perl-DBD-SQLite
Version:        1.58
Release:        2%{?dist}
Group:          Development/Libraries
License:        (GPL+ or Artistic) and Public Domain
URL:            http://search.cpan.org/dist/DBD-SQLite/
Source0:        https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/DBD-SQLite-%{version}.tar.gz
%define sha1    DBD-SQLite=060575ccf965a80e02b4caed40c1ef589532cf52
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  sqlite-devel >= 3.22.0
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-DBI
Requires:       perl-DBI
Requires:       perl >= 5.28.0

%description
SQLite is a public domain RDBMS database engine that you can find at
http://www.hwaci.com/sw/sqlite/.

This module provides a SQLite RDBMS module that uses the system SQLite
libraries.

%prep
%setup -q -n DBD-SQLite-%{version}

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
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.58-2
-   Cross compilation support
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.58-1
-   Update to version 1.58
*   Tue Feb 20 2018 Xiaolin Li <xiaolinl@vmware.com> 1.54-2
-   Build perl-DBD-SQLite with sqlite-autoconf-3.22.0.
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 1.54-1
-   Upgraded to 1.54
*   Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 1.50-3
-   Use sqlite-devel as a BuildRequires
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.50-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.50-1
-   Upgraded to version 1.50
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.48-1
-   Upgrade version
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.46-1
-   Initial version.
