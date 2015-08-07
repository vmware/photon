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
Requires:	bash glibc libgcc 

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

%package perl
Summary: openssl perl scripts
Group: Applications/Internet
Requires: perl
Requires: openssl = %{version}-%{release}
%description perl
Perl scripts that convert certificates and keys to various formats.

%prep
%setup -q

%build
export CFLAGS="%{optflags}"
./config \
	--prefix=%{_prefix} \
	--libdir=lib \
	--openssldir=/%{_sysconfdir}/ssl \
	shared \
	zlib-dynamic \
	-Wa,--noexecstack "${CFLAGS}" "${LDFLAGS}"
# does not support -j yet
make
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make INSTALL_PREFIX=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=ssl install
ln -sf %{_libdir}/libssl.so.1.0.0 %{buildroot}%{_libdir}/libssl.so.1.0.2

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/ssl/certs
%{_sysconfdir}/ssl/misc/CA.sh
%{_sysconfdir}/ssl/misc/c_hash
%{_sysconfdir}/ssl/misc/c_info
%{_sysconfdir}/ssl/misc/c_issuer
%{_sysconfdir}/ssl/misc/c_name
%{_sysconfdir}/ssl/openssl.cnf
%{_sysconfdir}/ssl/private
%{_bindir}/openssl
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

%files perl
/%{_bindir}/c_rehash
/%{_sysconfdir}/ssl/misc/tsget
/%{_sysconfdir}/ssl/misc/CA.pl

%changelog
*   Fri Aug 07 2015 Sharath George <sharathg@vmware.com> 1.0.2d-2
-   Split perl scripts to a different package.
*   Fri Jul 24 2015 Chang Lee <changlee@vmware.com> 1.0.2d-1
-   Update new version.
*	Wed Mar 25 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.2a-1
-	Initial build.	First version
