Name:           perl-HTTP-Message
Version:        6.45
Release:        1%{?dist}
Summary:        HTTP style message
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND CC0-1.0
URL:            https://metacpan.org/release/HTTP-Message
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Message-%{version}.tar.gz
%define sha512 HTTP-Message=b72ab9068c5f9ddb41f89b2a84887393f2c1bd14b462a1a60c03b4560800cfbf37c76f4bdd7c08f1ce9bf616242c2e39e0ff93859ed61268c48c978322a6d03d

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl

Requires: perl
Requires: perl-Clone
Requires: perl-URI

# Remove underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Clone|Exporter|HTTP::Date|URI)\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(HTTP::Headers\\)$
# Remove private modules and unused dependencies
%global __requires_exclude %{__requires_exclude}|^perl\\((Secret|Time::Local)\\)
%global __provides_exclude %{__provides_exclude}|^perl\\(Secret\\)$

%description
The HTTP-Message distribution contains classes useful for representing the
messages passed in HTTP style communication.  These are classes representing
requests, responses and the headers contained within them.

%prep
%autosetup -p1 -n HTTP-Message-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} %{?_smp_mflags}
%{_fixperms} %{buildroot}/*

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
%make_build test

%files
%license LICENSE
%doc Changes CONTRIBUTING.md README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Oct 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.45-1
- Intial version. Needed by perl-Crypt-SSLeay.
