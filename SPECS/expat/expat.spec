Summary:	An XML parser library
Name:		expat
Version:	2.1.0
Release:	2%{?dist}
License:	MIT
URL:		http://expat.sourceforge.net/
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/%{name}-%{version}.tar.gz
%define sha1 expat=b08197d146930a5543a7b99e871cba3da614f6f0
%description
The Expat package contains a stream oriented C library for parsing XML.

%package devel
Summary: Development libraries and header files for the expat library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The expat-devel contains the development libraries and header files for
expat.

%prep
%setup -q
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
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
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/*


%changelog
*   Wed Oct 14 2015 Xiaolin Li <xiaolinl@vmware.com> 2.1.0-2
-   Move development libraries and header files to devel package.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.0-1
-	Initial build.	First version
