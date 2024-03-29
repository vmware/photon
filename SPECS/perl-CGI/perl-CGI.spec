Summary:        Handle Common Gateway Interface requests and responses
Name:           perl-CGI
Version:        4.54
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CGI
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://cpan.metacpan.org/authors/id/L/LE/LEEJO/CGI-%{version}.tar.gz
%define sha512 CGI=be7ecdd9eab81ad95d527aac2f10ef7a15322675fe002558c6ab4951f496a8964025b7d0426241fb3f61aba103964a40f99acc05a39c84a2434f70d90ac47be6

BuildArch:      noarch

BuildRequires:  perl
BuildRequires:  (coreutils or coreutils-selinux)
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  sed

Requires:       perl

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
%autosetup -p1 -n CGI-%{version}
iconv -f iso8859-1 -t utf-8 < Changes > Changes.1
mv Changes.1 Changes
sed -i 's?usr/bin perl?usr/bin/perl?' t/init.t
chmod -c -x examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan Test::Deep
cpan HTML::Entities
cpan Test::Warn
cpan Test::NoWarnings
make %{?_smp_mflags} test
%endif

%files
%defattr(-,root,root)
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.54-2
- Fix build requires
* Thu Dec 08 2022 Gerrit Photon <photon-checkins@vmware.com> 4.54-1
- Automatic Version Bump
* Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 4.50-1
- Automatic Version Bump
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 4.40-1
- Update to version 4.40
* Mon Apr 3 2017 Robert Qi <qij@vmware.com> 4.35-1
- Upgraded to 4.35
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.26-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.26-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.26-1
- Updated to version 4.26
* Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 4.25-1
- Initial version.
