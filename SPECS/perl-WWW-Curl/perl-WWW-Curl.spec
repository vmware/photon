# Got the intial spec from Fedora and modified it
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)

Summary:        Perl extension interface for libcurl
Name:           perl-WWW-Curl
Version:        4.17
Release:        5%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/WWW-Curl/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SZ/SZBALINT/WWW-Curl-%{version}.tar.gz
%define sha1    WWW-Curl=8ec7b7b39bd653539671fb02fbb7d0ff4863e636
Patch0:         perl-www-curl-curl-7.66.0-compatibility.patch
Patch1:         Define-CURL-as-void.patch
Patch2:         Skip-preprocessor-symbol-only-CURL_STRICTER.patch
Patch3:         Adapt-to-changes-in-cURL.patch
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  perl
BuildRequires:  perl-Module-Install
BuildRequires:  perl-YAML-Tiny
BuildRequires:  curl-devel
Requires:       perl
Requires:       curl
%description
WWW::Curl is a Perl extension interface for libcurl.

%prep
%setup -q -n WWW-Curl-%{version}
rm -rf inc && sed -i -e '/^inc\//d' MANIFEST
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
# These tests require network, use "--with network_tests" to execute them
%{?!_with_network_tests: rm t/01basic.t }
%{?!_with_network_tests: rm t/02callbacks.t }
%{?!_with_network_tests: rm t/04abort-test.t }
%{?!_with_network_tests: rm t/05progress.t }
%{?!_with_network_tests: rm t/08ssl.t }
%{?!_with_network_tests: rm t/09times.t }
%{?!_with_network_tests: rm t/14duphandle.t }
%{?!_with_network_tests: rm t/15duphandle-callback.t }
%{?!_with_network_tests: rm t/18twinhandles.t }
%{?!_with_network_tests: rm t/19multi.t }
%{?!_with_network_tests: rm t/21write-to-scalar.t }
make test

%files
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/WWW*
%{_mandir}/man3/*

%changelog
*   Mon Mar 29 2021 Harinadh D <hdommaraju@vmware.com> 4.17-5
-   Build WWW-Curl with curl 7.75.0
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 4.17-4
-   BuildRequires curl-devel.
*   Thu Sep 15 2016 Xiaolin Li <xiaolinl@vmware.com> 4.17-3
-   Build WWW-Curl with curl 7.50.3
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.17-2
-   GA - Bump release of all rpms
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 4.17-1
-   Initial version.

