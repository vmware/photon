Summary:        A CBOR parsing C library
Name:           libcbor
Version:        0.9.0
Release:        1%{?dist}
License:        MIT
URL:            http://libcbor.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/PJK/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=710239f69d770212a82e933e59df1aba0fb3ec516ef6666a366f30a950565a52981b0d46ca7e0eea739f5785d79cc21fc19acd857a4a0b135f4f6aa3ef5fd3b0

BuildRequires:	glibc-devel
BuildRequires:	cmake

Requires:  glibc

%description
libcbor is a C library for parsing and generating CBOR, the general-purpose schema-less binary data format.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
%{name}-devel contains the development libraries and header files for %{name}.

%prep
%autosetup -p1

%build
%cmake -B . -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFFIX=%{_usr} ./
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE.md
%doc README.md
%{_libdir}/libcbor.so
%{_libdir}/libcbor.so.0*

%files devel
%defattr(-,root,root)
%{_includedir}/cbor.h
%{_includedir}/cbor/*.h
%{_includedir}/cbor/internal/*.h
%{_libdir}/pkgconfig/libcbor.pc

%changelog
* Fri May 13 2022 Nitesh Kumar <kunitesh@vmware.com> 0.9.0-1
- Initial version
