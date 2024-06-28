Name:           perl-Data-Dump
Version:        1.25
Release:        1%{?dist}
Summary:        Pretty printing of data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Data-Dump
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://cpan.metacpan.org/modules/by-module/Data/Data-Dump-%{version}.tar.gz
%define sha512 Data-Dump=fc859b0f02a44a959da3e162606c8fbaefececf8dbd0aa357d68a5a3143b818ae423dd7862063f2f77161ea000fcaa6841c96a2c4a268b889da9588292b157fe

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl

Requires: perl

%description
This module provides a single function called dump() that takes a list of
values as its argument and produces a string as its result. The string
contains Perl code that, when evaled, produces a deep copy of the original
arguments. The string is formatted for easy reading.

%prep
%autosetup -p1 -n Data-Dump-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} %{?_smp_mflags}
%{_fixperms} -c %{buildroot}

%check
%make_build test

%files
%doc Changes README.md
%{perl_vendorlib}/Data/
%{_mandir}/man3/Data::Dump.3*
%{_mandir}/man3/Data::Dump::Filtered.3*
%{_mandir}/man3/Data::Dump::Trace.3*

%changelog
* Sun Oct 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.25-1
- Intial version. Needed by perl-Crypt-SSLeay.
