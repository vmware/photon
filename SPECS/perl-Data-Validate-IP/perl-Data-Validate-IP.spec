%global build_if %{photon_subrelease} >= 91

Summary:        IPv4 and IPv6 validation methods
Name:           perl-Data-Validate-IP
Version:        0.31
Release:        2%{?dist}
Group:          Development/Libraries
URL:            https://metacpan.org/release/Data-Validate-IP
Source0:        https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Data-Validate-IP-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl >= 5.42.2
Requires:       perl >= 5.42.2
BuildRequires:  perl-NetAddr-IP
Requires:       perl-NetAddr-IP

%description
This module provides a number IP address validation subs that both
validate and untaint their input. This includes both basic validation
(is_ipv4() and is_ipv6()) and special cases like checking whether an
address belongs to a specific network or whether an address is public
or private (reserved).

%prep
%autosetup -n Data-Validate-IP-%{version}
rm -f Changes CODE_OF_CONDUCT.md  CONTRIBUTING.md INSTALL
%if 0%{?with_check} == 0
  rm -rf t/ xt/
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
# Install the required perl module - Test::Requires
export PERL_MM_USE_DEFAULT=1
echo "yes" | cpan -a
cpan -i Test::Requires
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Apr 01 2026 Dweep Advani <dweep.advani@broadcom.com> 0.31-2
- Bump for upgrading perl to 5.42.2
* Wed Jun 11 2025 Dweep Advani <dweep.advani@broadcom.com> 0.31-1
- Upgrade to 0.31
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 0.30-2
- Release bump for SRP compliance
* Thu Dec 08 2022 Gerrit Photon <photon-checkins@vmware.com> 0.30-1
- Automatic Version Bump
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 0.27-3
- Rebuilding for perl version 5.30.1
* Mon Dec 03 2018 Dweep Advani <dadvani@vmware.com> 0.27-2
- Fixing the makecheck tests
* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.27-1
- Initial version.
