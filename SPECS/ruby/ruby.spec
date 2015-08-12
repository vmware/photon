Summary:	Ruby
Name:		ruby
Version:	2.2.1
Release:	1%{?dist}
License:	BSDL
URL:		https://www.ruby-lang.org/en/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://cache.ruby-lang.org/pub/ruby/2.2/%{name}-%{version}.tar.gz
%define sha1 ruby=12376b79163e02bc9bd1a39329d67c3d19ccace9
BuildRequires:	openssl-devel
BuildRequires:	ca-certificates
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
*   Tue Apr 28 2015 Fabio Rapposelli <fabio@vmware.com> 2.2.1-2
-   Added SSL support
*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.1-1
-   Version upgrade to 2.2.1
*	Thu Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.3-1
-	Initial build.	First version
