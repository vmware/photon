# Got the intial spec from Fedora and modified it
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Devel::PPPort|ExtUtils::MakeMaker|File::Remove|File::Spec|YAML::Tiny)\\)$

Summary:        Standalone, extensible Perl module installer
Name:           perl-Module-Install
Version:        1.14
Release:        1
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Install/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/Module-Install-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:	perl

%description
Module::Install is a package for writing installers for CPAN (or CPAN-like)
distributions that are clean, simple, minimalist, act in a strictly correct
manner with ExtUtils::MakeMaker, and will run on any Perl installation
version 5.005 or newer.

%prep
%setup -q -n Module-Install-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
rm -rf %{buildroot}/blib/lib/auto/share/dist/Module-Install/dist_file.txt
%{_fixperms} %{buildroot}/*

%check
make test AUTOMATED_TESTING=1

%files
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.14-1
-	Initial version.

