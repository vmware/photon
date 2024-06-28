Summary:        Google's data interchange format - C implementation
Name:           protobuf-c
Version:        1.4.1
Release:        1%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/protobuf-c/protobuf-c

Source0: https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.3/%{name}-%{version}.tar.gz
%define sha512 %{name}=57f858118a89befc80e111ad9a57eadbcf2317d60e085b6d99e10f6604ee8c08473fe6ab1fdfb0a3196821a6e68e743943338321d23d15a1229987f140341181

BuildRequires:  protobuf-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libstdc++
BuildRequires:  curl
BuildRequires:  make
BuildRequires:  unzip

Requires:       protobuf >= 3.21.12

%description
Protocol Buffers (a.k.a., protobuf) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. You can find protobuf's documentation on the Google Developers site. This is the C implementation.

%package        devel
Summary:        Development files for protobuf
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        static
Summary:        %{name} static lib
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    static
The %{name}-static package contains static %{name} libraries.

%prep
%autosetup -p1

%build
autoreconf -fvi
%configure \
    --disable-silent-rules \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/protoc-c
%{_libdir}/libprotobuf-c.so.*
%{_bindir}/protoc-gen-c

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libprotobuf-c.so

%files static
%defattr(-,root,root)

%changelog
* Sat Jun 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.4.1-1
- Upgrade to v1.4.1
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.3-3
- Remove .la files
* Fri Feb 19 2021 Harinadh D <hdommaraju@vmware.com> 1.3.3-2
- Version bump up to build with latest protobuf
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.3-1
- Automatic Version Bump
* Wed Sep 19 2018 Tapas Kundu <tkundu@vmware.com> 1.3.1-1
- Updated to release 1.3.1
* Thu Mar 30 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2.1-2
- Fix protobuf-c-static requires
* Sat Mar 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2.1-1
- Initial packaging for Photon
