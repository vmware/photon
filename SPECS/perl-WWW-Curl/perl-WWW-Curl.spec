%define srcname WWW-Curl

# Got the intial spec from Fedora and modified it
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)

Summary:        Perl extension interface for libcurl
Name:           perl-WWW-Curl
Version:        4.17
Release:        9%{?dist}
License:        MIT
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/WWW-Curl
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://search.cpan.org/CPAN/authors/id/S/SZ/SZBALINT/WWW-Curl-%{version}.tar.gz
%define sha512 %{srcname}=bc7a75d0e23f5a77578fd7244b56a1e1b81d814993b90ac7132926f0d571232c4c95875bc615cb6239e424ae1d5481d27796efc5376bb0845d1da0ff1137c0d6

Patch0: perl-www-curl-curl-7.66.0-compatibility.patch
Patch1: Define-CURL-as-void.patch
Patch2: Skip-preprocessor-symbol-only-CURL_STRICTER.patch
Patch3: Adapt-to-changes-in-cURL.patch
Patch4: WWW-Curl-4.17-Adapt-to-curl-8.0.1.patch

BuildRequires: perl
BuildRequires: perl-Module-Install
BuildRequires: perl-YAML-Tiny
BuildRequires: curl-devel

Requires: perl
Requires: curl

%description
WWW::Curl is a Perl extension interface for libcurl.

%prep
%autosetup -p1 -n %{srcname}-%{version}
rm -rf inc
sed -i -e '/^inc\//d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
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
%make_buildtest
%endif

%files
%defattr(-,root,root)
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/WWW*
%{_mandir}/man3/*

%changelog
* Thu Jul 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.17-9
- Fix build error with latest curl
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 4.17-8
- Perl version upgrade to 5.36.0
* Mon Sep 21 2020 Dweep Advani <dadvani@vmware.com> 4.17-7
- Rebuilding for perl 5.30.1
* Wed Sep 02 2020 Ankit Jain <ankitja@vmware.com> 4.17-6
- Fix Build issue with curl-7.72.0 version
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 4.17-5
- Consuming perl version upgrade of 5.28.0
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 4.17-4
- BuildRequires curl-devel.
* Thu Sep 15 2016 Xiaolin Li <xiaolinl@vmware.com> 4.17-3
- Build WWW-Curl with curl 7.50.3
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.17-2
- GA - Bump release of all rpms
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 4.17-1
- Initial version.
