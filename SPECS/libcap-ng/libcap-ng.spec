Summary:	POSIX capability Library
Name:		libcap-ng
Version:	0.7.7
Release:	2%{?dist}
License: 	LGPLv2+
Group: 		System Environment/Libraries
URL: 		http://people.redhat.com/sgrubb/libcap-ng
Source0: 	http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
%define sha1 libcap-ng=de8ea2c89cb1506a578de7cb032da34c970dd035
BuildRequires:	python2-devel
BuildRequires:	python2-libs
Requires:	python2

%description
The libcap-ng library is intended to make programming with posix capabilities much easier than the traditional libcap library. It includes utilities that can analyse all currently running applications and print out any capabilities and whether or not it has an open ended bounding set. An open bounding set without the securebits "NOROOT" flag will allow full capabilities escalation for apps retaining uid 0 simply by calling execve.

%package devel
Summary:	The libraries and header files needed for libcap-ng development.
Requires: 	%{name} = %{version}-%{release}

%description devel
The libraries and header files needed for libcap_ng development.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--with-python \
	--without-python3

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install 

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_libdir}/*.la
%{_bindir}/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%{_datadir}/aclocal/*.m4

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.7-2
-	GA - Bump release of all rpms
* 	Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 0.7.7-1
- 	Initial version

