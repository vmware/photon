Name:           perl-libwww-perl
Version:        6.72
Release:        2%{?dist}
Summary:        A Perl interface to the World-Wide Web
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/libwww-perl
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://cpan.metacpan.org/authors/id/O/OA/OALDERS/libwww-perl-%{version}.tar.gz
%define sha512 libwww-perl=2dd7052e2105b7bc8abe81742707e6a9aa9891316755171c275e8f547c65f97354a133027eeac93f1a1657ae986bdd9a74a9c887518acb8b5ea634e96910e57d

BuildArch:      noarch

BuildRequires:  coreutils >= 9.1-7
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl

Requires: perl
Requires: perl-URI
Requires: perl-Try-Tiny
Requires: perl-Data-Dump
Requires: perl-HTTP-Message
Requires: perl-Clone
Requires: perl-HTTP-Date

%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Authen::NTLM|Encode|File::Listing|HTTP::Cookies|HTTP::Daemon|HTTP::Date|HTTP::Negotiate|HTTP::Request|HTTP::Response|HTTP::Status|LWP::MediaTypes|MIME::Base64|Net::FTP|Net::HTTP|Test::More|URI|WWW::RobotRules|Encode::Locale)\\)$

%description
The libwww-perl collection is a set of Perl modules which provides a simple and
consistent application programming interface to the World-Wide Web.  The main
focus of the library is to provide classes and functions that allow you to
write WWW clients. The library also contain modules that are of more general
use and even classes that help you implement simple HTTP servers.

%prep
%autosetup -p1 -n libwww-perl-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 --aliases < /dev/null
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
unset COVERAGE PERL_LWP_ENV_HTTP_TEST_SERVER_TIMEOUT PERL_LWP_ENV_HTTP_TEST_URL
%make_build test

%files
%defattr(-,root,root)
%license LICENSE
%doc Changes examples README.SSL
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Wed Oct 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.72-2
- Require coreutils only
* Sun Oct 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.72-1
- Intial version. Needed by perl-Crypt-SSLeay.
