%global build_if %{photon_subrelease} >= 91

Summary:        ExtUtils::InstallPaths - Build.PL install path logic made easy
Name:           perl-ExtUtils-InstallPaths
Version:        0.015
Release:        1%{?dist}
Group:          Development/Libraries
URL:            https://metacpan.org/pod/ExtUtils::InstallPaths
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-InstallPaths-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl >= 5.42.2
Requires:       perl >= 5.42.2
Requires:       perl-ExtUtils-Config

%description
This module tries to make install path resolution as easy as possible.

%prep
%autosetup -n ExtUtils-InstallPaths-%{version}
#%if 0%{?with_check} == 0
#  rm -rf Changes CONTRIBUTING testrules.yml t/ xt/
#%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/*
%{_mandir}/man3/ExtUtils::InstallPaths.3.gz

%changelog
* Thu Apr 30 2026 Dweep Advani <dweep.advani@broadcom.com> 0.015-1
- Introduce ExtUtils::InstallPaths needed by perl-Module-Build 0.42_35
