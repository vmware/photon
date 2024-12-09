# Got the intial spec from Fedora and modified it
Summary:       Simple data types for common serialization formats
Name:          perl-Types-Serialiser
Version:       1.01
Release:       2%{?dist}
Group:         Development/Libraries
URL:           http://search.cpan.org/dist/Types-Serialiser/
Source0:       http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/Types-Serialiser-%{version}.tar.gz
%define sha512 Types-Serialiser=419b24cae85fba045de2f4593e1d17784f2016d5f9cd9ea96d23bbeaa86c1c6b866875871a787cacba1299616d371cc8806760e4c53e4f635deec4bc28fa81b5

Source1: license.txt
%include %{SOURCE1}
Vendor:        VMware, Inc.
Distribution:  Photon
BuildArch:     noarch
BuildRequires: perl
Requires:      perl
BuildRequires: perl-common-sense
Requires:      perl-common-sense

# Filter bogus provide of JSON::PP::Boolean (for rpm ≥ 4.9)
%global __provides_exclude ^perl\\(JSON::PP::Boolean\\)

%description
This module provides some extra data types that are used by common
serialization formats such as JSON or CBOR. The idea is to have a repository of
simple/small constants and containers that can be shared by different
implementations so they become interoperable between each other.

%prep
%autosetup -n Types-Serialiser-%{version}

# Filter bogus provide of JSON::PP::Boolean (for rpm < 4.9)
%global provfilt /bin/sh -c "%{__perl_provides} | grep -v '^perl(JSON::PP::Boolean)'"
%define __perl_provides %{provfilt}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}

%files
%{perl_vendorlib}/Types/
%{_mandir}/man3/*

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.01-2
- Release bump for SRP compliance
* Thu Dec 08 2022 Gerrit Photon <photon-checkins@vmware.com> 1.01-1
- Automatic Version Bump
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 1.0-4
- Rebuilding for perl 5.30.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.0-3
- Consuming perl version upgrade of 5.28.0
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-2
- GA - Bump release of all rpms
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.0-1
- Initial version.
