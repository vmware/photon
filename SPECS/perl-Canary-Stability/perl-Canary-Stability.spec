Summary:        Canary to check perl compatibility for Schmorp's modules
Name:           perl-Canary-Stability
Version:        2013
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Canary-Stability/
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/Canary-Stability-%{version}.tar.gz
%define sha512  Canary-Stability=9dfb0e6d136048050aac7c29e1fc79dc2a7703c8800582aa837c5d9b9934c48bfcb0a9ef1c6b5bb7e71a10a709e7f7431b3c79ea12b8d9f374b33bfd4a3e468d
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:       perl

%description
This module is used by Schmorp's modules during configuration stage to test
the installed perl for compatibility with his modules.

%prep
%autosetup -n Canary-Stability-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}

%files
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
*   Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 2013-2
-   Perl version upgrade to 5.36.0
*   Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 2013-1
-   Automatic Version Bump
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2012-2
-   Consuming perl version upgrade of 5.28.0
* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 2012-1
-   Initial version.
