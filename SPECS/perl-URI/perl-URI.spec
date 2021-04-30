Summary:        A Perl module implementing URI parsing and manipulation
Name:           perl-URI
Version:        5.09
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            https://metacpan.org/release/URI
Source0:        https://cpan.metacpan.org/modules/by-module/URI/perl-URI-%{version}.tar.gz
%define sha1    perl-URI=ee3a28661467ea086c69edaece4746002b380d6d
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  perl
BuildRequires:  make
BuildRequires:  perl-Module-Install

Requires:       perl

%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396
(andupdated by RFC 2732).

%global debug_package %{nil}

%prep
%setup -q -n URI-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=true NO_PERLLOCAL=true
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*
%files
%license LICENSE
%doc Changes CONTRIBUTING.md README uri-test
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Apr 30 2021 Susant Sahani <ssahani@vmware.com> 5.09-1
- Initial version.

