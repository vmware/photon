Summary:        Manages IPv4 and IPv6 addresses and subnets
Name:           perl-NetAddr-IP
Version:        4.079
Release:        4%{?dist}
Group:          Development/Libraries
URL:            https://metacpan.org/release/NetAddr-IP
Source0:        https://cpan.metacpan.org/authors/id/M/MI/MIKER/NetAddr-IP-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
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
*   Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 4.079-4
-   Release bump for SRP compliance
*   Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 4.079-3
-   Perl version upgrade to 5.36.0
*   Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 4.079-2
-   Rebuilding for perl version 5.30.1
*   Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.079-1
-   Initial version.
