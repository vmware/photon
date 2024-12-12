Summary:        Wrapper Class for the various JSON classes
Name:           perl-JSON-Any
Version:        1.39
Release:        7%{?dist}
Group:          Development/Libraries
URL:            http://search.cpan.org/~ether/JSON-Any-1.39/lib/JSON/Any.pm
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/JSON-Any-%{version}.tar.gz
%define sha512  JSON-Any=a4e9494ef650fe6f0144fddad49962e717470390b5783ab7bed6ef1c34fa7aa3d4f8699b9967ec8ca8813f43ee8c1d594e5af4d4962929791aa95b470104cd9b

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
Requires:       perl
BuildRequires:  perl

%description
This module tries to provide a coherent API to bring together the various JSON modules currently on CPAN. This module will allow you to code to any JSON API and have it work regardless of which JSON module is actually installed.

%prep
%autosetup -n JSON-Any-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
            -name '*.bs' -size 0 \) -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%check
export PERL_MM_USE_DEFAULT=1
cpan Test::Fatal  Test::Requires Test::Warnings Test::Without::Module
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.39-7
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 1.39-6
- Perl version upgrade to 5.36.0
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 1.39-5
- Rebuilding for perl 5.30.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.39-4
- Consuming perl version upgrade of 5.28.0
* Tue Aug 08 2017 Chang Lee <Chang Lee@vmware.com> 1.39-3
- Adding dependencies for %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.39-2
- GA - Bump release of all rpms
* Mon Mar 28 2016 Mahmoud Bassiouny <mbassiounu@vmware.com> 1.39-1
- Initial version.
