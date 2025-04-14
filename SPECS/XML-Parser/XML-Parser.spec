Summary:       XML-Parser perl module
Name:          XML-Parser
Version:       2.46
Release:       6%{?dist}
URL:           http://search.cpan.org/~toddr/%{name}-%{version}/
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: http://search.cpan.org/CPAN/authors/id/T/TO/TODDR/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: expat-devel
BuildRequires: perl

Requires:      expat
Requires:      perl

%description
The XML::Parser module is a Perl extension interface to James Clark's XML parser, expat

%prep
%autosetup

%build
perl Makefile.PL
if [ %{_host} != %{_build} ]; then
  ln -s /target-%{_arch}%{perl_privlib}/%{_arch}-linux %{perl_privlib}/%{_arch}-linux
  mkdir -p %{perl_vendorlib}
  ln -s /target-%{_arch}%{perl_vendorlib}/%{_arch}-linux %{perl_vendorlib}/%{_arch}-linux

  # ugly hack again, similarly to cmake:
  ln -sf %{_arch}-linux-gnu-gcc /usr/bin/gcc
  ln -sf %{_arch}-linux-gnu-g++ /usr/bin/g++
  ln -sf %{_arch}-linux-gnu-ld /usr/bin/ld
  ln -sf %{_arch}-linux-gnu-ar /usr/bin/ar
fi
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%define __perl_version 5.36.0
rm %{buildroot}/%{_libdir}/perl5/%{__perl_version}/*/perllocal.pod

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%{_libdir}/perl5/*
%{_mandir}/man3/*

%changelog
* Wed Apr 09 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.46-6
- Version bump for expat upgrade
* Mon Dec 16 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.46-5
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.46-4
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 2.46-3
- Perl version upgrade to 5.36.0
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 2.46-2
- Rebuild for perl version upgrade to 5.30.1
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 2.46-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 2.44-6
- Cross compilation support
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2.44-5
- Consuming perl version upgrade of 5.28.0
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.44-4
- Aarch64 support
* Tue Apr 4 2017 Robert Qi <qij@vmware.com> 2.44-3
- Update to version 2.44-3 since perl version updated.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.44-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.44-1
- Upgraded to version 2.44
* Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 2.41-3
- Fix for multithreaded perl
* Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 2.41-2
- Fix for new perl
* Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.41-1
- Initial build. First version
