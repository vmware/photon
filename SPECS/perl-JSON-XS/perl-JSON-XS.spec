# Got the intial spec from Fedora and modified it
Summary:        JSON serializing/deserializing, done correctly and fast
Name:           perl-JSON-XS
Epoch:          1
Version:        4.03
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/JSON-XS/
Source0:        https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/JSON-XS-%{version}.tar.gz
%define sha512  JSON-XS=7d2c20302b0f98bd69e692b61d272b58c13a79741f3e2e44ee0530e21dd239526477f8b02e4afbfe41ee83cb69ab1c5247bf0be355f3f09e9cfe31b2ea4a5155
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  perl
BuildRequires:  perl-Canary-Stability
BuildRequires:  perl-Types-Serialiser
BuildRequires:  perl-common-sense
Requires:       perl
Requires:       perl-Canary-Stability
Requires:       perl-Types-Serialiser
Requires:       perl-common-sense

%description
This module converts Perl data structures to JSON and vice versa. Its
primary goal is to be correct and its secondary goal is to be fast. To
reach the latter goal it was written in C.

%prep
%autosetup -n JSON-XS-%{version}

sed -i 's/\r//' t/*
perl -pi -e 's|^#!/opt/bin/perl|#!%{__perl}|' eg/*
chmod -c -x eg/*

%build
export PERL_CANARY_STABILITY_NOPROMPT=1
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} test

%files
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_bindir}/*
%{_mandir}/man[13]/*

%changelog
* Thu Dec 08 2022 Gerrit Photon <photon-checkins@vmware.com> 4.03-1
- Automatic Version Bump
* Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 4.02-1
- Automatic Version Bump
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 3.04-1
- Update to version 3.04
* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 3.03-1
- Add build requires for perl-Canary-Stability, and pass NO_PACKLIST to Makefile.PL.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.01-2
- GA - Bump release of all rpms
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 3.01-1
- Initial version.
