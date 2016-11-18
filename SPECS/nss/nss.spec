Summary:	Security client
Name:		nss
Version:	3.25
Release:	3%{?dist}
License:	MPLv2.0
URL:		http://ftp.mozilla.org/pub/mozilla.org/security/nss
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	%{name}-%{version}.tar.gz
%define sha1 nss=ffa55041a7904bb43afbc6821f479819d9802abf
Patch:		nss-3.25-standalone-1.patch
Requires:	nspr
BuildRequires:	nspr
BuildRequires:	sqlite-devel
Requires:	sqlite-libs

%description
 The Network Security Services (NSS) package is a set of libraries
 designed to support cross-platform development of security-enabled
 client and server applications. Applications built with NSS can
 support SSL v2 and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12,
 S/MIME, X.509 v3 certificates, and other security standards.
 This is useful for implementing SSL and S/MIME or other Internet
 security standards into an application.

%package devel
Summary: Development Libraries for Network Security Services
Group: Development/Libraries
Requires: nss = %{version}-%{release}
%description devel
Header files for doing development with Network Security Services.

%prep
%setup -q
%patch -p1
%build
cd nss
# -j is not supported by nss
make VERBOSE=1 BUILD_OPT=1 \
	NSPR_INCLUDE_DIR=%{_includedir}/nspr \
	USE_SYSTEM_ZLIB=1 \
	ZLIB_LIBS=-lz \
	$([ $(uname -m) = x86_64 ] && echo USE_64=1) \
	$([ -f %{_includedir}/sqlite3.h ] && echo NSS_USE_SYSTEM_SQLITE=1)
%install
cd nss
cd ../dist
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_includedir}/nss
install -vdm 755 %{buildroot}%{_libdir}
install -v -m755 Linux*/lib/*.so %{buildroot}%{_libdir}
install -v -m644 Linux*/lib/{*.chk,libcrmf.a} %{buildroot}%{_libdir}
cp -v -RL {public,private}/nss/* %{buildroot}%{_includedir}/nss
chmod 644 %{buildroot}%{_includedir}/nss/*
install -v -m755 Linux*/bin/{certutil,nss-config,pk12util} %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_libdir}/pkgconfig
install -vm 644 Linux*/lib/pkgconfig/nss.pc %{buildroot}%{_libdir}/pkgconfig

%check
cd nss/tests
HOST=localhost DOMSUF=localdomain
./all.sh

%post	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.chk
%{_libdir}/*.so

%files devel
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc


%changelog
*	Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.25-3
-	Use sqlite-libs as runtime dependency
*       Mon Oct 04 2016 ChangLee <changLee@vmware.com> 3.25-2
-       Modified %check
*       Tue Jul 05 2016 Anish Swaminathan <anishs@vmware.com> 3.25-1
-       Upgrade to 3.25
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.21-2
-	GA - Bump release of all rpms
* 	Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 3.21
- 	Updated to version 3.21
*       Tue Aug 04 2015 Kumar Kaushik <kaushikk@vmware.com> 3.19-2
-       Version update. Firefox requirement.
*	Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19-1
-	Version update. Firefox requirement.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.15.4-1
-	Initial build. First version
