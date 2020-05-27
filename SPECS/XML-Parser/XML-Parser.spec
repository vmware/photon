Summary:	XML-Parser perl module
Name:		XML-Parser
Version:	2.44
Release:	5%{?dist}
License:	GPL+
URL:		http://search.cpan.org/~toddr/%{name}-%{version}/
Source0:		http://search.cpan.org/CPAN/authors/id/T/TO/TODDR/%{name}-%{version}.tar.gz
%define sha1 XML-Parser=0ab6b932713ec1f9927a1b1c619b6889a5c12849
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	expat-devel
BuildRequires:	perl >= 5.28.0
Requires:	expat
Requires:	perl >= 5.28.0
%description
The XML::Parser module is a Perl extension interface to James Clark's XML parser, expat
%prep
%setup -q
%build
perl Makefile.PL --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%define __perl_version 5.28.0
rm %{buildroot}/%{_libdir}/perl5/%{__perl_version}/*/perllocal.pod

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%{_libdir}/perl5/*
%{_mandir}/man3/*
%changelog
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2.44-5
-   Consuming perl version upgrade of 5.28.0
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.44-4
-   Aarch64 support
*   Tue Apr 4 2017 Robert Qi <qij@vmware.com> 2.44-3
-   Update to version 2.44-3 since perl version updated.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.44-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.44-1
-   Upgraded to version 2.44
*   Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 2.41-3
-   Fix for multithreaded perl
*   Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 2.41-2
-   Fix for new perl
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.41-1
-   Initial build. First version
