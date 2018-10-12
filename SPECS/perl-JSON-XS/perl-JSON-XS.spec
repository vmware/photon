# Got the intial spec from Fedora and modified it
Summary:        JSON serializing/deserializing, done correctly and fast
Name:           perl-JSON-XS
Epoch:          1
Version:        3.04
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/JSON-XS/
Source0:        https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/JSON-XS-%{version}.tar.gz
%define sha1 JSON-XS=582f874f3c4ad8a0bbf6986f7af2676a92e91b8a
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-Canary-Stability
BuildRequires:  perl-Types-Serialiser
BuildRequires:  perl-common-sense
Requires:  perl >= 5.28.0
Requires:  perl-Canary-Stability
Requires:  perl-Types-Serialiser
Requires:  perl-common-sense

%description
This module converts Perl data structures to JSON and vice versa. Its
primary goal is to be correct and its secondary goal is to be fast. To
reach the latter goal it was written in C.

%prep
%setup -q -n JSON-XS-%{version}

sed -i 's/\r//' t/*
perl -pi -e 's|^#!/opt/bin/perl|#!%{__perl}|' eg/*
chmod -c -x eg/*

%build
export PERL_CANARY_STABILITY_NOPROMPT=1
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_bindir}/*
%{_mandir}/man[13]/*

%changelog
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 3.04-1
-   Update to version 3.04
*   Wed Apr 05 2017 Robert Qi <qij@vmware.com> 3.03-1
-   Add build requires for perl-Canary-Stability, and pass NO_PACKLIST to Makefile.PL.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.01-2
-   GA - Bump release of all rpms
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 3.01-1
-   Initial version.
