Summary:    Ruby
Name:       ruby
Version:    2.4.0
Release:    5%{?dist}
License:    BSDL
URL:        https://www.ruby-lang.org/en/
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    http://cache.ruby-lang.org/pub/ruby/%{version}/%{name}-%{version}.tar.gz
%define sha1 ruby=d44a3c50a0e742341ed3033d5db79d865151a4f4
Patch0:     ruby-CVE-2017-9224.patch
Patch1:     ruby-CVE-2017-9226.patch
Patch2:     ruby-CVE-2017-9227.patch
Patch3:     ruby-CVE-2017-9229.patch
Patch4:	    ruby-CVE-2017-6181.patch
Patch5:	    ruby-CVE-2017-9228.patch
BuildRequires:  openssl-devel
BuildRequires:  ca-certificates
BuildRequires:  readline-devel
BuildRequires:  readline
Requires:   ca-certificates
Requires:   openssl
Requires:   gmp
%description
The Ruby package contains the Ruby development environment.
This is useful for object-oriented scripting.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%build
./configure \
    --prefix=%{_prefix}   \
        --enable-shared \
        --docdir=%{_docdir}/%{name}-%{version}
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/ruby/*
%{_datadir}/ri/*
%{_docdir}/%{name}-%{version}
%{_mandir}/man1/*
%changelog
*   Tue Aug 08 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.0-5
-   [security] CVE-2017-9228
*   Fri Jul 07 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.4.0-4
-   [security] ruby-CVE-2017-6181.patch
*   Tue Jun 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.0-3
-   [security] CVE-2017-9224,CVE-2017-9225
-   [security] CVE-2017-9227,CVE-2017-9229
*   Wed May 31 2017 Divya Thaluru <dthaluru@vmware.com> 2.4.0-2
-   Bump release to build with latest openssl
*   Wed Jan 18 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0-1
-   Update to 2.4.0 - Fixes CVE-2016-2339
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.0-3
-   GA - Bump release of all rpms
*   Wed Mar 09 2016 Divya Thaluru <dthaluru@vmware.com> 2.3.0-2
-   Adding readline support
*   Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.0-1
-   Updated to 2.3.0-1
*   Tue Apr 28 2015 Fabio Rapposelli <fabio@vmware.com> 2.2.1-2
-   Added SSL support
*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.1-1
-   Version upgrade to 2.2.1
*   Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.3-1
-   Initial build.  First version
