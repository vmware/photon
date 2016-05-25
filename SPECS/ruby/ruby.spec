Summary:	Ruby
Name:		ruby
Version:	2.3.0
Release:	3%{?dist}
License:	BSDL
URL:		https://www.ruby-lang.org/en/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://cache.ruby-lang.org/pub/ruby/2.3/%{name}-%{version}.tar.gz
%define sha1 ruby=2dfcf7f33bda4078efca30ae28cb89cd0e36ddc4
BuildRequires:	openssl-devel
BuildRequires:	ca-certificates
BuildRequires:	readline-devel
BuildRequires:	readline
Requires:	ca-certificates
Requires:	openssl
Requires:	gmp
%description
The Ruby package contains the Ruby development environment.
This is useful for object-oriented scripting.

%prep
%setup -q
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
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/ruby/*
%{_datadir}/ri/*
%{_docdir}/%{name}-%{version}
%{_mandir}/man1/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	2.3.0-3
-	GA - Bump release of all rpms
*   Tue Mar 09 2016 Divya Thaluru <dthaluru@vmware.com> 2.3.0-2
-   Adding readline support
*   Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.0-1
-   Updated to 2.3.0-1
*   Tue Apr 28 2015 Fabio Rapposelli <fabio@vmware.com> 2.2.1-2
-   Added SSL support
*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.1-1
-   Version upgrade to 2.2.1
*	Thu Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.3-1
-	Initial build.	First version
