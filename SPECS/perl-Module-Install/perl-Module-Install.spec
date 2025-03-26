# Got the intial spec from Fedora and modified it
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Devel::PPPort|ExtUtils::MakeMaker|File::Remove|File::Spec|YAML::Tiny)\\)$

Summary:        Standalone, extensible Perl module installer
Name:           perl-Module-Install
Version:        1.19
Release:        4%{?dist}
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Install/
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/Module-Install-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-YAML-Tiny
Requires:       perl-YAML-Tiny
Requires:       perl

%description
Module::Install is a package for writing installers for CPAN (or CPAN-like)
distributions that are clean, simple, minimalist, act in a strictly correct
manner with ExtUtils::MakeMaker, and will run on any Perl installation
version 5.005 or newer.

%prep
%autosetup -n Module-Install-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
rm -rf %{buildroot}/blib/lib/auto/share/dist/Module-Install/dist_file.txt
%{_fixperms} %{buildroot}/*

%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan File::Remove
make %{?_smp_mflags} test AUTOMATED_TESTING=1

%files
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
*   Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.19-4
-   Release bump for SRP compliance
*   Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 1.19-3
-   Perl version upgrade to 5.36.0
*   Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 1.19-2
-   Rebuilding for perl 5.30.1
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.19-1
-   Update to version 1.19
*   Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.18-1
-   Update version to 1.18.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.16-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.16-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com> 1.16-1
-   Upgrade version to 1.16
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.14-1
-   Initial version.
