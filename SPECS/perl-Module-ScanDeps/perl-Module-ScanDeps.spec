# Got the intial spec from Fedora and modified it
Summary:        Recursively scan Perl code for dependencies
Name:           perl-Module-ScanDeps
Version:        1.18
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/R/RS/RSCHUPP/Module-ScanDeps-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Module-ScanDeps/
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:	perl

%description
This module scans potential modules used by perl programs and returns a
hash reference.  Its keys are the module names as they appear in %%INC (e.g.
Test/More.pm).  The values are hash references.

%prep
%setup -q -n Module-ScanDeps-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
%{_fixperms} %{buildroot}

%check
make test

%files
%{_bindir}/scandeps.pl
%{perl_vendorlib}/Module/
%{_mandir}/man1/scandeps.pl.1*
%{_mandir}/man3/*

%changelog
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.18-1
-	Initial version.
