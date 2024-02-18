Summary:        multi-platform support library with a focus on asynchronous I/O
Name:           libuv
Version:        1.34.2
Release:        4%{?dist}
URL:            https://codeload.github.com/libuv/libuv
License:        MIT, BSD and ISC
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/libuv/libuv/archive/%{name}-%{version}.tar.gz
%define sha512 libuv=7e7a54d2d1e0ed76654ece9481f02177d201a4590c5d9b5c8b4edf6f795a0d7c30970b907481847930a524a0f06c15c6c73b3ce73a8afa2f836e33dbd54a7249

Patch0:         0001-unix-don-t-use-_POSIX_PATH_MAX.patch
Patch1:         CVE-2024-24806.patch
%description
libuv is a multi-platform support library with a focus on asynchronous I/O. It was primarily developed for use by Node.js, but it's also used by Luvit, Julia, pyuv, and others.
%package    devel
Summary:    Header and development files for zlib
Requires:   %{name} = %{version}-%{release}
%description    devel
Development libraries for libuv

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure
make V=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_includedir}/uv/*.h
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun Feb 18 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.34.2-4
- Fix CVE-2024-24806
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.34.2-3
- Fix CVE-2020-8252
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.34.2-2
- Remove .la files
* Mon Feb 17 2020 Sujay G <gsujay@vmware.com> 1.34.2-1
- Initial build. First version
