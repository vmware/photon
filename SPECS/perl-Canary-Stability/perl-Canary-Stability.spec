Summary:        Canary to check perl compatibility for Schmorp's modules
Name:           perl-Canary-Stability
Version:        2013
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Canary-Stability/
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/Canary-Stability-%{version}.tar.gz
%define sha1 Canary-Stability=b20e8478a0658634e12d2cbc33b449450760af19
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:       perl

%description
This module is used by Schmorp's modules during configuration stage to test
the installed perl for compatibility with his modules.

%prep
%setup -q -n Canary-Stability-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
*   Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 2013-1
-   Automatic Version Bump
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2012-2
-   Consuming perl version upgrade of 5.28.0
* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 2012-1
-   Initial version.
