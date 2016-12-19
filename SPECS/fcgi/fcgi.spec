Summary:	FastCGI development kit
Name:		fcgi
Version:	2.4.0
Release:	1%{?dist}
License:	BSD
URL:		http://www.fastcgi.com
Source0:	http://fastcgi.com/dist/fcgi-%{version}.tar.gz
%define sha1 fcgi=2329404159e8b8315e524b9eaf1de763202c6e6a
Patch0:		fcgi-EOF.patch
Group:		Development/Libraries/C and C++
Vendor:		VMware, Inc.
Distribution:	Photon

%description
FastCGI is a language independent, scalable, open extension to CGI that
provides high performance without the limitations of server specific APIs.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
FastCGI is a language independent, scalable, open extension to CGI that
provides high performance without the limitations of server specific APIs.

%prep
%setup -q 
%patch0 -p1

%build
./configure \
	--prefix=%{_prefix} \
	--disable-static
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.a' -delete
find %{buildroot}/%{_libdir} -name '*.la' -delete

%check
make check 

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libfcgi.so*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
*	Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 2.4.0-1
-	Initial build. First version
