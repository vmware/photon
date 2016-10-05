# Got the intial spec from Fedora and modified it

Summary:        Handle Common Gateway Interface requests and responses
Name:           perl-CGI
Version:        4.26
Release:        3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/L/LE/LEEJO/CGI-%{version}.tar.gz
URL:            http://search.cpan.org/dist/CGI
%define sha1 CGI=fb3bcc43d832e22ca794ae8b81be69820ac52b20
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  sed
Requires:	perl

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((File::Spec)\\)$
# Remove false dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Fh)\\)
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(MultipartBuffer\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Fh\\)

%description
CGI.pm is a stable, complete and mature solution for processing and preparing
HTTP requests and responses. Major features including processing form
submissions, file uploads, reading and writing cookies, query string
generation and manipulation, and processing and preparing HTTP headers. Some
HTML generation utilities are included as well.

CGI.pm performs very well in in a vanilla CGI.pm environment and also comes 
with built-in support for mod_perl and mod_perl2 as well as FastCGI.

%prep
%setup -q -n CGI-%{version}
iconv -f iso8859-1 -t utf-8 < Changes > Changes.1
mv Changes.1 Changes
sed -i 's?usr/bin perl?usr/bin/perl?' t/init.t
chmod -c -x examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}/*

%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan Test::Deep
cpan HTML::Entities
cpan Test::Warn
cpan Test::NoWarnings
make %{?_smp_mflags} test

%files
%license LICENSE
%doc Changes README.md examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.26-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.26-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.26-1
-   Updated to version 4.26
*	Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 4.25-1
-	Initial version.

