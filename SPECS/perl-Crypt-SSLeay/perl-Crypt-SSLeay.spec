Summary:        Crypt::SSLeay - OpenSSL support for LWP
Name:           perl-Crypt-SSLeay
Version:        0.72
Release:        2%{?dist}
URL:            http://search.cpan.org/dist/Crypt-SSLeay/
License:        Perl Artistic License 2.0
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         http://search.cpan.org/CPAN/authors/id/N/NA/NANIS/Crypt-SSLeay-%{version}.tar.gz
%define sha1    Crypt-SSLeay=1b39920947c33a88b19a9c8e61ccb135b56091f8

BuildArch:      x86_64
Requires:       perl
Requires:       openssl
BuildRequires:  perl
BuildRequires:  openssl-devel
BuildRequires:  perl-Path-Class
BuildRequires:  perl-Try-Tiny

%description
This Perl module provides support for the HTTPS protocol under LWP, to allow an LWP::UserAgent object to perform GET, HEAD and POST requests. Please see LWP for more information on POST requests.

The Crypt::SSLeay package provides Net::SSL, which is loaded by LWP::Protocol::https for https requests and provides the necessary SSL glue.

This distribution also makes following deprecated modules available:

Crypt::SSLeay::CTX
Crypt::SSLeay::Conn
Crypt::SSLeay::X509
Work on Crypt::SSLeay has been continued only to provide https support for the LWP (libwww-perl) libraries.

%prep
%setup -q -n Crypt-SSLeay-%{version}

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
sed -i 's/CCCDLFLAGS = /CCCDLFLAGS = -g /' Makefile
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
            -name '*.bs' -size 0 \) -exec rm -f {} ';'

%check
make test

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.72-2
-   Fix arch
*   Wed Apr 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.72-1
-   Initial version.

