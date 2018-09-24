Summary:        Minimal try/catch with proper preservation of $@
Name:           perl-Try-Tiny
Version:        0.30
Release:        1%{?dist}
URL:            http://search.cpan.org/~ether/Try-Tiny-0.28/
License:        The MIT (X11) License
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         https://cpan.metacpan.org/authors/id/E/ET/ETHER/Try-Tiny-%{version}.tar.gz
%define sha1    Try-Tiny=4f0edb634a2b4c032c55ef9ab90dd8bbe7780afd

BuildArch:      noarch
Requires:       perl >= 5.28.0
BuildRequires:  perl >= 5.28.0

%description
This module provides bare bones try/catch/finally statements that are designed to minimize common mistakes with eval blocks, and NOTHING else.

This is unlike TryCatch which provides a nice syntax and avoids adding another call stack layer, and supports calling return from the try block to return from the parent subroutine. These extra features come at a cost of a few dependencies, namely Devel::Declare and Scope::Upper which are occasionally problematic, and the additional catch filtering uses Moose type constraints which may not be desirable either.

%prep
%setup -q -n Try-Tiny-%{version}

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make test

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.30-1
-   Update to version 0.30
*   Wed Apr 26 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.28-2
-   Fix arch
*   Wed Apr 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.28-1
-   Initial version.
