%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Devel::PPPort|ExtUtils::MakeMaker|File::Remove|File::Spec|YAML::Tiny)\\)$

Summary:        Standalone, extensible Perl module installer
Name:           perl-Module-Install
Version:        1.19
Release:        4%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Install
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://cpan.metacpan.org/authors/id/E/ET/ETHER/Module-Install-%{version}.tar.gz
%define sha512 Module-Install=68a255402c98955cfcb5a8a99555fe511b89d5fccf96ee1c498cab347c8945f3abe53485ea936f7419420d9c7beb52c861516f4cfd299812cebf80eab50fa5ba

BuildArch:      noarch

BuildRequires:  perl
BuildRequires:  perl-YAML-Tiny

Requires:       perl
Requires:       perl-YAML-Tiny
Requires:       perl-File-Remove

%description
Module::Install is a package for writing installers for CPAN (or CPAN-like)
distributions that are clean, simple, minimalist, act in a strictly correct
manner with ExtUtils::MakeMaker, and will run on any Perl installation
version 5.005 or newer.

%prep
%autosetup -p1 -n Module-Install-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install %{?_smp_mflags} pure_install
find %{buildroot} -type f -name .packlist -delete
rm -f %{buildroot}/blib/lib/auto/share/dist/Module-Install/dist_file.txt
%{_fixperms} %{buildroot}/*

%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan File::Remove
%make_build test AUTOMATED_TESTING=1

%files
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Oct 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.19-4
- Add File-Remove to requires
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 1.19-3
- Perl version upgrade to 5.36.0
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 1.19-2
- Rebuilding for perl 5.30.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.19-1
- Update to version 1.19
* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.18-1
- Update version to 1.18.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.16-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.16-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com> 1.16-1
- Upgrade version to 1.16
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.14-1
- Initial version.
