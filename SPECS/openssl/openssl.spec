Summary:	Management tools and libraries relating to cryptography
Name:		openssl
Version:	1.0.2d
Release:	2%{?dist}
License:	OpenSSL
URL:		http://www.openssl.org
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.openssl.org/source/%{name}-%{version}.tar.gz
%define sha1 openssl=d01d17b44663e8ffa6a33a5a30053779d9593c3d

%description
The OpenSSL package contains management tools and libraries relating
to cryptography. These are useful for providing cryptography 
functions to other packages, such as OpenSSH, email applications and
web browsers (for accessing HTTPS sites).

%package devel
Summary: Development Libraries for openssl
Group: Development/Libraries
Requires: openssl = %{version}-%{release}
%description devel
Header files for doing development with openssl.


%prep
%setup -q

%build
export CFLAGS="%{optflags}"
./config \
	--prefix=%{_prefix} \
	--libdir=lib \
	--openssldir=/etc/ssl \
	shared \
	zlib-dynamic \
	-Wa,--noexecstack "${CFLAGS}" "${LDFLAGS}"
# does not support -j yet
make
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make INSTALL_PREFIX=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=ssl install
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/etc/ssl/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/engines/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files devel
%{_includedir}/*
%{_mandir}/man3*/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
*       Thu Jul 28 2015 Chang Lee <changlee@vmware.com> 1.0.2b-1
-	Update new version.
*	Wed Mar 25 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.2a-1
-	Initial build.	First version
