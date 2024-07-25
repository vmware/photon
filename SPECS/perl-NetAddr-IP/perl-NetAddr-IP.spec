Summary:        Manages IPv4 and IPv6 addresses and subnets
Name:           perl-NetAddr-IP
Version:        4.079
Release:        3%{?dist}
License:        GPLv2+ or Artistic
Group:          Development/Libraries
URL:            https://metacpan.org/release/NetAddr-IP
Source0:        https://cpan.metacpan.org/authors/id/M/MI/MIKER/NetAddr-IP-%{version}.tar.gz
%define sha512  NetAddr-IP=8ebc8ffb914cf72c041441f96de0e9c982eebdb8c26dbf15f885d0113b3634e4851d81f13f555c14d1fdf0ab95ae2ce880ed124e6c200e391adae3b1d6d3eb65
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  perl
Requires:       perl

%description
This module provides an object-oriented abstraction on top of IP
addresses or IP subnets, that allows for easy manipulations.

%prep
%autosetup -n NetAddr-IP-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
*   Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 4.079-3
-   Perl version upgrade to 5.36.0
*   Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 4.079-2
-   Rebuilding for perl version 5.30.1
*   Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.079-1
-   Initial version.
