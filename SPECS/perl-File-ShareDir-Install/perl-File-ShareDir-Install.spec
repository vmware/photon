%global build_if %{photon_subrelease} >= 91

Summary:        File::ShareDir::Install - Install shared files
Name:           perl-File-ShareDir-Install
Version:        0.14
Release:        1%{?dist}
Group:          Development/Libraries
URL:            https://metacpan.org/pod/File::ShareDir::Install
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/File-ShareDir-Install-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl >= 5.42.2
Requires:       perl >= 5.42.2

%description
File::ShareDir::Install allows you to install read-only data files from a
distribution. It is a companion module to File::ShareDir, which allows you to
locate these files after installation.

%prep
%autosetup -n File-ShareDir-Install-%{version}
%if 0%{?with_check} == 0
  rm -rf Changes CONTRIBUTING testrules.yml t/ xt/
%endif

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
%{_mandir}/man3/File::ShareDir::Install.3.gz

%changelog
* Thu Apr 30 2026 Dweep Advani <dweep.advani@broadcom.com> 0.14-1
- Introduce File::ShareDir::Install needed by XML-Parser 2.57 while building
