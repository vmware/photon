Summary:	A portable, high level programming interface to various calling conventions
Name:		libffi
Version:	3.2.1
Release:	6%{?dist}
License:	BSD
URL:		http://sourceware.org/libffi/
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://sourceware.org/pub/libffi/%{name}-%{version}.tar.gz
%define sha1 libffi=280c265b789e041c02e5c97815793dfc283fb1e6
Provides:	pkgconfig(libffi)
%if %{with_check}
BuildRequires:  dejagnu
%endif

%description
The libffi library provides a portable, high level programming interface
to various calling conventions. This allows a programmer to call any 
function specified by a call interface description at run time.

%package    devel
Summary:    Header and development files for libffi
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications 

%prep
%setup -q

%build
sed -e '/^includesdir/ s:$(libdir)/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:$(includedir):' \
    -i include/Makefile.in &&
sed -e '/^includedir/ s:${libdir}/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:@includedir@:' \
    -e 's/^Cflags: -I${includedir}/Cflags:/' \
    -i libffi.pc.in        &&
%configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static \
    --target=%{_target}
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
find %{buildroot} -name '*.la' -delete
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%ifarch %{ix86}
%{_libdir}/*.so*
%else
%{_lib64dir}/*.so*
%endif

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datarootdir}/licenses/libffi/LICENSE
%{_mandir}/man3/*

%changelog
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-6
-   Aarch64 support
*   Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-5
-   Get tcl, expect and dejagnu from packages
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-4
-   Added -devel subpackage
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 3.2.1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.1-2
-   GA - Bump release of all rpms
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 3.2.1-1
-   Updated to version 3.2.1
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.1-1
-   Initial build.	First version
