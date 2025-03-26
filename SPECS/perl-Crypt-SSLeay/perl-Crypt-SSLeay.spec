Summary:        Crypt::SSLeay - OpenSSL support for LWP
Name:           perl-Crypt-SSLeay
Version:        0.72
Release:        9%{?dist}
URL:            http://search.cpan.org/dist/Crypt-SSLeay/
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://search.cpan.org/CPAN/authors/id/N/NA/NANIS/Crypt-SSLeay-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
%autosetup -n Crypt-SSLeay-%{version}

%build
PERL5LIB=$(pwd) env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
sed -i 's/CCCDLFLAGS = /CCCDLFLAGS = -g /' Makefile
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot} -type f \( -name .packlist -o \
            -name '*.bs' -size 0 \) -exec rm -f {} ';'

%check
make test %{?_smp_mflags}

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 0.72-9
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 0.72-8
- Perl version upgrade to 5.36.0
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.72-7
- Bump up release for openssl
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.72-6
- openssl 1.1.1
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 0.72-5
- Rebuilding for perl 5.30.1
* Tue Nov 20 2018 Dweep Advani <dadvani@vmware.com> 0.72-4
- Reverting to 0.72 as 0.73_06 is still a DEV version
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.73_06-1
- Update version to 0.73_06
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.72-3
- Remove BuildArch
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.72-2
- Fix arch
* Wed Apr 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.72-1
- Initial version.
