# Got the intial spec from Fedora and modified it
Summary:	Simple data types for common serialization formats
Name:		perl-Types-Serialiser
Version:	1.0
Release:	2%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Types-Serialiser/
Source0:	http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/Types-Serialiser-%{version}.tar.gz
%define sha1 Types-Serialiser=72ba9d1d97bb582360c79bcbdb158e73573adb70
Vendor:		VMware, Inc.
Distribution:	Photon 
BuildArch:	noarch
BuildRequires:	perl
Requires:	perl
BuildRequires:	perl-common-sense
Requires:	perl-common-sense

# Filter bogus provide of JSON::PP::Boolean (for rpm ≥ 4.9)
%global __provides_exclude ^perl\\(JSON::PP::Boolean\\)

%description
This module provides some extra data types that are used by common
serialization formats such as JSON or CBOR. The idea is to have a repository of
simple/small constants and containers that can be shared by different
implementations so they become interoperable between each other.

%prep
%setup -q -n Types-Serialiser-%{version}

# Filter bogus provide of JSON::PP::Boolean (for rpm < 4.9)
%global provfilt /bin/sh -c "%{__perl_provides} | grep -v '^perl(JSON::PP::Boolean)'"
%define __perl_provides %{provfilt}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}

%files
%{perl_vendorlib}/Types/
%{_mandir}/man3/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-2
-	GA - Bump release of all rpms
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.0-1
-	Initial version.
