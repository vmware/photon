Summary:	An URL retrieval utility and library
Name:		curl
Version:	7.43.0
Release:	2%{?dist}
License:	MIT
URL:		http://curl.haxx.se
Group:		System Environment/NetworkingLibraries
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://curl.haxx.se/download/%{name}-%{version}.tar.lzma
%define sha1 curl=22d7646741f22cc4c7ca8d72a1ef089d5f2b94a7
Requires:	ca-certificates
BuildRequires:	ca-certificates
Requires:	openssl
BuildRequires:	openssl-devel
%description
The cURL package contains an utility and a library used for 
transferring files with URL syntax to any of the following 
protocols: FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, 
DICT, LDAP, LDAPS and FILE. Its ability to both download and 
upload files can be incorporated into other programs to support
functions like streaming media.

%package devel
Summary:	The libraries and header files needed for %{name} development.
Requires: 	%{name} = %{version}-%{release}

%description devel
The libraries and header files needed for%{name} development.

%prep
%setup -q
sed -i '/--static-libs)/{N;s#echo .*#echo #;}' curl-config.in
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--disable-static \
	--enable-threaded-resolver \
	--with-ssl \
	--with-ca-bundle=/etc/pki/tls/certs/ca-bundle.crt
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -v -d -m755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datarootdir}/aclocal/libcurl.m4
%{_docdir}/%{name}-%{version}

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so

%changelog
*   Wed Oct 14 2015 Xiaolin Li <xiaolinl@vmware.com> 7.43.0-2
-   Move development libraries and header files to devel package.
*	Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 7.43.0-1
-	Update to version 7.43.0.
*	Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.41.0-1
-	Update to version 7.41.0.
