Summary:        Perl extension for using OpenSSL
Name:           perl-Net-SSLeay
Version:        1.85
Release:        1%{?dist}
License:        Perl Artistic License 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/~mikem/Net-SSLeay-%{version}/
Source:         https://cpan.metacpan.org/authors/id/M/MI/MIKEM/Net-SSLeay-%{version}.tar.gz
%define sha1 Net-SSLeay=5f1c7b6ccac81efd5b78b1e076c694f96ca5c439
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       perl
Requires:       openssl
BuildRequires:  perl
BuildRequires:  openssl-devel

%description
Net::SSLeay module contains perl bindings to openssl (http://www.openssl.org) library.

Net::SSLeay module basically comprise of:
* High level functions for accessing web servers (by using HTTP/HTTPS)
* Low level API (mostly mapped 1:1 to openssl's C functions)
* Convenience functions (related to low level API but with more perl friendly interface)
* There is also a related module called Net::SSLeay::Handle included in this distribution that you might want to use instead. It has its own pod documentation.

%prep
%setup -q -n Net-SSLeay-%{version}

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete

%check
make test

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
*   Thu Sep 20 2018 Dweep Advani <dadvani@vmware.com> 1.85-1
-   Update to version 1.85
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.81-2
-   Remove BuildArch
*   Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.81-1
-   Update version to 1.81
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.72-2
-   GA - Bump release of all rpms
*   Mon Mar 28 2016 Mahmoud Bassiouny <mbassiounu@vmware.com> 1.72-1
-   Initial version.

