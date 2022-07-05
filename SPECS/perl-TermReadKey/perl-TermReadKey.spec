Name:          perl-TermReadKey
Version:       2.38
Release:       1%{?dist}
Summary:       TermReadKey Perl module
License:       GPL+ or Artistic
Group:         Development/Perl
Vendor:        VMware, Inc.
Distribution:  Photon
Url:           https://metacpan.org/release/TermReadKey
Source0:       https://cpan.metacpan.org/authors/id/J/JS/JSTOWE/TermReadKey-%{version}.tar.gz
%define sha512 TermReadKey=fb09f013f9f0d8a4397e39f6f3db7a6d023259219af8f76744094e396437a01b19141b3cdb39a158d3b518903fb010088bc37406763bfbeb3fcab810bb0bb157
BuildRequires: perl
BuildRequires: perl-List-MoreUtils
Requires:      perl

%description
TermReadKey module provides ioctl control for terminals so the input modes
can be changed, and also provides non-blocking reads of stdin, as well
as several other terminal related features, including retrieval/modification
of the screen size, and retrieval/modification of the control characters

%prep
%autosetup -n TermReadKey-%{version}
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1

%build
%make_build

%install
%make_install

%files
%defattr(-,root,root,-)
%doc README
%{perl_vendorarch}/*
%{_mandir}/man3/*

%changelog
* Tue May 24 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.38-1
- perl-TermReadKey initial build
