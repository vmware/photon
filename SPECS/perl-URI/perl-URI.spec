Summary:        A Perl module implementing URI parsing and manipulation
Name:           perl-URI
Version:        5.17
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            https://metacpan.org/release/URI
Source0:        https://cpan.metacpan.org/modules/by-module/URI/perl-URI-%{version}.tar.gz
%define sha512  perl-URI=52171e16137bfaa77ab31007245a561614c5c42336473022ebbe370b395d3052d3de80da0b42754ca2e0b09f47520ef96afdbdb72fe5c25cab87441eda03ec12
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
%autosetup -n URI-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=true NO_PERLLOCAL=true
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%files
%license LICENSE
%doc Changes CONTRIBUTING.md README uri-test
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 5.17-1
- Version upgrade to 5.17
* Fri Apr 30 2021 Susant Sahani <ssahani@vmware.com> 5.09-1
- Initial version.
