Summary:        IPv4 and IPv6 validation methods
Name:           perl-Data-Validate-IP
Version:        0.27
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            https://metacpan.org/release/Data-Validate-IP
Source0:        https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Data-Validate-IP-%{version}.tar.gz
%define sha1    Data-Validate-IP=da24fd6404359e475f65d35cb4341db74c48f48a
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:       perl
BuildRequires:  perl-NetAddr-IP
Requires:       perl-NetAddr-IP

%description
This module provides a number IP address validation subs that both
validate and untaint their input. This includes both basic validation
(is_ipv4() and is_ipv6()) and special cases like checking whether an
address belongs to a specific network or whether an address is public
or private (reserved).

%prep
%setup -q -n Data-Validate-IP-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
# Install the required perl module - Test::Requires
export PERL_MM_USE_DEFAULT=1
echo "yes" | cpan -a
cpan -i Test::Requires
make test

%files
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
*   Mon Dec 03 2018 Dweep Advani <dadvani@vmware.com> 0.27-2
-   Fixing the makecheck tests
*   Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.27-1
-   Initial version.
