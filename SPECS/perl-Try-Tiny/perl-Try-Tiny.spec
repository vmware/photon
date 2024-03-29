Summary:        Minimal try/catch with proper preservation of $@
Name:           perl-Try-Tiny
Version:        0.31
Release:        1%{?dist}
URL:            http://search.cpan.org/~ether/Try-Tiny-0.28/
License:        The MIT (X11) License
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         https://cpan.metacpan.org/authors/id/E/ET/ETHER/Try-Tiny-%{version}.tar.gz
%define sha512  Try-Tiny=1a3c852e56797d81da60a4f4887cb70fc575eca83d10b8cd12fe5d5d0008a967801218f3a5277a2f1347ade95b9515c1f237333e491742d06614c0beecf44768

BuildArch:      noarch
Requires:       perl
BuildRequires:  perl

%description
This module provides bare bones try/catch/finally statements that are designed to minimize common mistakes with eval blocks, and NOTHING else.

This is unlike TryCatch which provides a nice syntax and avoids adding another call stack layer, and supports calling return from the try block to return from the parent subroutine. These extra features come at a cost of a few dependencies, namely Devel::Declare and Scope::Upper which are occasionally problematic, and the additional catch filtering uses Moose type constraints which may not be desirable either.

%prep
%autosetup -n Try-Tiny-%{version}

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Thu Dec 08 2022 Gerrit Photon <photon-checkins@vmware.com> 0.31-1
- Automatic Version Bump
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 0.30-2
- Rebuilding for perl 5.30.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.30-1
- Update to version 0.30
* Wed Apr 26 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.28-2
- Fix arch
* Wed Apr 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.28-1
- Initial version.
