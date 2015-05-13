Summary:	Management tools and libraries relating to cryptography
Name:		openssl
Version:	1.0.2a
Release:	1
License:	OpenSSL
URL:		http://www.openssl.org
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.openssl.org/source/%{name}-%{version}.tar.gz
Patch0:		openssl-1.0.2a-fix_parallel_build-1.patch
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
%patch0 -p1
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
/usr/share/man/man3/.3ssl.gz

%files devel
%{_includedir}/*
%{_mandir}/man3*/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
*	Wed Mar 25 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.2a-1
-	Initial build.	First version
