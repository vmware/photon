# Got the intial spec from Fedora and modified it
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((ExtUtils::Install|File::Spec|Module::Build|Module::Metadata|Perl::OSType)\\)$
%global __requires_exclude %__requires_exclude|^perl\\(CPAN::Meta::YAML\\) >= 0.002$

Summary:        Build and install Perl modules
Name:           perl-Module-Build
Version:        0.4231
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Build/
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-%{version}.tar.gz
%define sha512 Module-Build=ee1dc18a7df3fe67e7f954d5e1e071aa0a6f5bce6783b768bceb01f071e64ac8be63f410c932c7c16764e5d4f52fc664ce11a12f26f6afc75a26f79883efad70
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:       perl

%description
Module::Build is a system for building, testing, and installing Perl
modules. It is meant to be an alternative to ExtUtils::MakeMaker.

%prep
%autosetup -n Module-Build-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

%check
rm t/signature.t
LANG=C TEST_SIGNATURE=1 MB_TEST_EXPERIMENTAL=1 ./Build test

%files
%doc Changes contrib LICENSE README
%{_bindir}/config_data
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
*   Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 0.4231-2
-   Perl upgrade to 5.36.0
*   Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4231-1
-   Automatic Version Bump
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.4224-1
-   Update to version 0.4224
*   Wed Apr 05 2017 Robert Qi <qij@vmware.com> 0.4222-1
-   Update version to 0.4222.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.4216-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.4216-1
-   Upgraded to version 0.4216
*   Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 0.4214-1
-   Initial version.
