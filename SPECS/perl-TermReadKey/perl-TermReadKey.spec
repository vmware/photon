Name:          perl-TermReadKey
Version:       2.38
Release:       3%{?dist}
Summary:       TermReadKey Perl module
Group:         Development/Perl
Vendor:        VMware, Inc.
Distribution:  Photon
Url:           https://metacpan.org/release/TermReadKey
Source0:       https://cpan.metacpan.org/authors/id/J/JS/JSTOWE/TermReadKey-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
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
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 2.38-3
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 2.38-2
- Perl version upgrade to 5.36.0
* Tue May 24 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.38-1
- perl-TermReadKey initial build
