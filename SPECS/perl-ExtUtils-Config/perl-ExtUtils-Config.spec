%global build_if %{photon_subrelease} >= 91

Summary:        ExtUtils::Config - A wrapper for perl's configuration
Name:           perl-ExtUtils-Config
Version:        0.010
Release:        1%{?dist}
Group:          Development/Libraries
URL:            https://metacpan.org/pod/ExtUtils::Config
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Config-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl >= 5.42.2
Requires:       perl >= 5.42.2

%description
ExtUtils::Config is an abstraction around the %Config hash. By itself it is not
a particularly interesting module by any measure, however it ties together a
 family of modern toolchain modules.

%prep
%autosetup -n ExtUtils-Config-%{version}
rm -f Changes INSTALL
%if 0%{?with_check} == 0
  rm -rf t/ xt/
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/*
%{_mandir}/man3/ExtUtils::Config.3.gz
%{_mandir}/man3/ExtUtils::Config::MakeMaker.3.gz

%changelog
* Thu Apr 30 2026 Dweep Advani <dweep.advani@broadcom.com> 0.010-1
- Introduce ExtUtils::Config needed by perl-Module-Build 0.42_35
