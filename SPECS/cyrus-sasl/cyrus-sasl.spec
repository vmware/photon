Summary:	Cyrus Simple Authentication Service Layer (SASL) library
Name:		cyrus-sasl
Version:	2.1.26
Release:	2%{?dist}
License:	Custom
URL:		http://cyrusimap.web.cmu.edu/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://ftp.cyrusimap.org/cyrus-sasl/%{name}-%{version}.tar.gz
%define sha1 cyrus-sasl=d6669fb91434192529bd13ee95737a8a5040241c
Source1:	http://www.linuxfromscratch.org/blfs/downloads/svn/blfs-bootscripts-20140919.tar.bz2
%define sha1 blfs-bootscripts=762b68f79f84463a6b1dabb69e9dbdc2c43f32d8
Patch0:		http://www.linuxfromscratch.org/patches/blfs/svn/cyrus-sasl-2.1.26-fixes-3.patch
Requires:	openssl
Requires:	krb5 >= 1.12
BuildRequires:	openssl-devel
BuildRequires:  krb5 >= 1.12
%description
The Cyrus SASL package contains a Simple Authentication and Security 
Layer, a method for adding authentication support to 
connection-based protocols. To use SASL, a protocol includes a command
for identifying and authenticating a user to a server and for 
optionally negotiating protection of subsequent protocol interactions.
If its use is negotiated, a security layer is inserted between the 
protocol and the connection.
%prep
%setup -q
%patch0 -p1
tar xf %{SOURCE1}
%build
autoreconf -fi
pushd saslauthd
autoreconf -fi
popd
./configure \
	CFLAGS="%{optflags} -fPIC" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc \
	--with-plugindir=%{_libdir}/sasl2 \
    --without-dblib \
    --without-saslauthd \
    --without-authdaemond \
    --disable-macos-framework \
    --disable-sample \
    --disable-cram \
    --disable-digest \
    --disable-otp \
    --disable-plain \
    --disable-anon \
    --enable-srp \
    --enable-gss_mutexes \
    --disable-static \
    --enable-shared \
    --enable-fast-install \
    --enable-krb4

make
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete
install -D -m644 COPYING %{buildroot}/usr/share/licenses/%{name}/LICENSE
#	daemonize
pushd blfs-bootscripts-20140919
make DESTDIR=%{buildroot} install-saslauthd
popd
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/etc/rc.d/init.d/saslauthd
/etc/rc.d/rc0.d/K49saslauthd
/etc/rc.d/rc1.d/K49saslauthd
/etc/rc.d/rc2.d/S24saslauthd
/etc/rc.d/rc3.d/S24saslauthd
/etc/rc.d/rc4.d/S24saslauthd
/etc/rc.d/rc5.d/S24saslauthd
/etc/rc.d/rc6.d/K49saslauthd
/etc/sysconfig/saslauthd
%{_includedir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_libdir}/sasl2/*
%{_sbindir}/*
%{_mandir}/man3/*
%{_datadir}/licenses/%{name}/LICENSE
%changelog
*	Thu Jul 16 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.26-2
-	Disabling parallel threads in make
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.26-1
-	Initial build.	First version
