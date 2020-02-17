Summary:        multi-platform support library with a focus on asynchronous I/O
Name:           libuv
Version:        1.34.2
Release:        1%{?dist}
URL:            https://github.com/libuv/
License:        MIT, BSD and ISC
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/libuv/libuv/archive/%{name}-%{version}.tar.gz
%define sha1    libuv=f59b25c0f1a855eef66298d65bd4fb288e0132b9

%description
libuv is a multi-platform support library with a focus on asynchronous I/O.
It was primarily developed for use by Node.js,
but it's also used by Luvit, Julia, pyuv, and others.

%package    devel
Summary:    Header and development files for zlib
Requires:   %{name} = %{version}
%description    devel
Development libraries for libuv

%prep
%setup -q

%build
./autogen.sh
%configure
make V=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_lib}

%check
make  %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/*.h
%{_includedir}/uv/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

%changelog
*   Mon Feb 17 2020 Sujay G <gsujay@vmware.com> 1.34.2-1
-   Initial build. First version
