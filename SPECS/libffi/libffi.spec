Summary:	A portable, high level programming interface to various calling conventions
Name:		libffi
Version:	3.1
Release:	2%{?dist}
License:	BSD
URL:		http://sourceware.org/libffi/
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://sourceware.org/pub/libffi/%{name}-%{version}.tar.gz
%define sha1 libffi=cb373ef2115ec7c57913b84ca72eee14b10ccdc3
Provides:	pkgconfig(libffi)
%description
The libffi library provides a portable, high level programming interface
to various calling conventions. This allows a programmer to call any 
function specified by a call interface description at run time.

%package devel
Summary: Development libraries and header files for the libffi library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
libffi-devel contains the development libraries and header files for
libffi.

%prep
%setup -q
%build
sed -e '/^includesdir/ s:$(libdir)/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:$(includedir):' \
    -i include/Makefile.in &&
sed -e '/^includedir/ s:${libdir}/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:@includedir@:' \
    -e 's/^Cflags: -I${includedir}/Cflags:/' \
    -i libffi.pc.in        &&
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
install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
%ifarch x86_64
find %{buildroot}/%{_lib64dir} -name '*.la' -delete
%else
find %{buildroot}/%{_libdir} -name '*.la' -delete
%endif
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%ifarch x86_64
%{_lib64dir}/*.so*
%else
%{_libdir}/*.so*
%endif
%{_datarootdir}/licenses/libffi/LICENSE
%{_mandir}/man3/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_includedir}/*


%changelog
*   Wed Oct 14 2015 Xiaolin Li <xiaolinl@vmware.com> 3.1-2
-   Move development libraries and header files to devel package.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.1-1
-	Initial build.	First version
