# Got the intial spec from Fedora and modified it

Summary:        Interface to create per object accessors
Name:           perl-Object-Accessor
Version:        0.48
Release:        3%{?dist}
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Object-Accessor/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/Object-Accessor-%{version}.tar.gz
%define sha1 Object-Accessor=0b97227252a0551c946b9f112a577b9d59ffd4ae
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
Requires:	perl >= 5.28.0

%description
Object::Accessor provides an interface to create per object accessors (as
opposed to per Class accessors, as, for example, Class::Accessor provides).

%prep
%setup -q -n Object-Accessor-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
*	Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.48-3
-	Consuming perl version upgrade of 5.28.0
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.48-2
-	GA - Bump release of all rpms
*	Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 0.48-1
-	Initial version.
