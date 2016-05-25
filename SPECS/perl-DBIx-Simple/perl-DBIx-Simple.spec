# Got the intial spec from Fedora and modified it
Summary:        Easy-to-use OO interface to DBI
Name:           perl-DBIx-Simple
Version:        1.35
Release:        2%{?dist}
License:        Public Domain
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/J/JU/JUERD/DBIx-Simple-%{version}.tar.gz 
%define sha1 DBIx-Simple=a6d08abf6dd3bfef7c337054beb49611572880b8
URL:            http://search.cpan.org/dist/DBIx-Simple/
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:      noarch
BuildRequires:  perl-DBI >= 1.21
BuildRequires:  perl
Requires:  	perl
Requires:  	perl-Object-Accessor
Requires:       perl-DBI >= 1.21

%description
DBIx::Simple provides a simplified interface to DBI, Perl's powerful
database module.

%prep
%setup -q -n DBIx-Simple-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.35-2
-	GA - Bump release of all rpms
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.35-1
-	Initial version.
