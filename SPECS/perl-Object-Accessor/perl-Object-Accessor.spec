# Got the intial spec from Fedora and modified it

Summary:        Interface to create per object accessors
Name:           perl-Object-Accessor
Version:        0.48
Release:        5%{?dist}
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Object-Accessor/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/Object-Accessor-%{version}.tar.gz
%define sha512  Object-Accessor=fbce10e8db2cfb360cdc093355a95c9d49909069beb725fca9812ee6e6b77e0648d63d56db9fbdcdf03f885b3954a67c516fa066229280279940704231d48448
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:       perl

%description
Object::Accessor provides an interface to create per object accessors (as
opposed to per Class accessors, as, for example, Class::Accessor provides).

%prep
%autosetup -n Object-Accessor-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} test

%files
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 0.48-5
- Perl version upgrade to 5.36.0
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 0.48-4
- Rebuilding for perl version 5.30.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.48-3
- Consuming perl version upgrade of 5.28.0
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.48-2
- GA - Bump release of all rpms
* Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 0.48-1
- Initial version.
