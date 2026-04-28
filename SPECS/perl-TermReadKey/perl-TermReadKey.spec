%global build_if %{photon_subrelease} >= 91

Name:          perl-TermReadKey
Version:       2.38
Release:       5%{?dist}
Summary:       TermReadKey Perl module
Group:         Development/Perl
Vendor:        VMware, Inc.
Distribution:  Photon
Url:           https://metacpan.org/release/TermReadKey
Source0:       https://cpan.metacpan.org/authors/id/J/JS/JSTOWE/TermReadKey-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires: perl >= 5.42.2
BuildRequires: perl-List-MoreUtils
Requires:      perl >= 5.42.2

%description
TermReadKey module provides ioctl control for terminals so the input modes
can be changed, and also provides non-blocking reads of stdin, as well
as several other terminal related features, including retrieval/modification
of the screen size, and retrieval/modification of the control characters

%prep
%autosetup -n TermReadKey-%{version}
%if 0%{?with_check} == 0
  for f in Changes; do
    sed -i -E "/^$f$/d" MANIFEST
    rm -f "$f"
  done
  for f in example t; do
    sed -i -E "/^$f\\/.*$/d" MANIFEST
    rm -rf "$f"
  done
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install

%files
%defattr(-,root,root,-)
%doc README
%{perl_vendorarch}/*
%{_mandir}/man3/*

%changelog
* Fri Apr 17 2026  Dweep Advani <dweep.advani@broadcom.com> 2.38-5
- Release bump for perl 5.42.2
* Wed Jun 11 2025  Dweep Advani <dweep.advani@broadcom.com> 2.38-4
- Release bump for perl 5.40.2
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 2.38-3
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 2.38-2
- Perl version upgrade to 5.36.0
* Tue May 24 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.38-1
- perl-TermReadKey initial build
