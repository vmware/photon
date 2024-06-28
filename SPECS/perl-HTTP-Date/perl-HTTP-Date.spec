Name:           perl-HTTP-Date
Version:        6.06
Release:        1%{?dist}
Summary:        Date conversion routines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/HTTP-Date
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Date-%{version}.tar.gz
%define sha512 HTTP-Date=e1555a9b5dff3b2041594f9b480f12a022eb03b0f1628f884fc88a3aed687ba7a6c7d743198c4ca7ba32df22a98fd070bd4a2bc2494703ec72e16303c9cfb3e6

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl

Requires: perl

# Remove under-specified version
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(Time::Local\\)$

%description
This module provides functions that deal the date formats used by the HTTP
protocol (and then some more). Only the first two functions, time2str() and
str2time(), are exported by default.

%prep
%autosetup -p1 -n HTTP-Date-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} %{?_smp_mflags}
%{_fixperms} %{buildroot}/*

%check
unset AUTHOR_TESTING PERL_COMPILE_TEST_DEBUG
%make_build test

%files
%license LICENSE
%doc Changes CONTRIBUTORS README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Oct 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.06-1
- Intial version. Needed by perl-Crypt-SSLeay.
