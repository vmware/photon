Summary:        multi-platform support library with a focus on asynchronous I/O
Name:           libuv
Version:        1.45.0
Release:        2%{?dist}
URL:            https://codeload.github.com/libuv/libuv
License:        MIT, BSD and ISC
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/libuv/libuv/archive/%{name}-%{version}.tar.gz
%define sha512  libuv=a156dd0ed06bc7c50515f46ef6e5636d870288636f442ce9ec46716e22fdaa664ce49e432f4737c81e9c6013b34ed150e7420ab9fc316ed23281096954359774

Patch0: CVE-2024-24806.patch

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
./autogen.sh
%configure
make V=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.a' -delete
find %{buildroot} -name '*.la' -delete
install -vdm 755 %{buildroot}/%{_lib}

%check
make  %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_includedir}/uv/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun Feb 18 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.45.0-2
- Fix CVE-2024-24806
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.45.0-1
- Update to v1.45.0
* Wed Jun 03 2020 Sujay G <gsujay@vmware.com> 1.34.2-1
- Initial build. First version
