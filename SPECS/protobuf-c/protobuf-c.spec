Summary:        Google's data interchange format - C implementation
Name:           protobuf-c
Version:        1.3.1
Release:        3%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/google/protobuf-c/
Source0:        %{name}-%{version}.tar.gz
%define         sha512 protobuf-c=555e6fdf303ddcd51516f9022d8c5e59304863930dfa6c5d4a5657356a444a9279dfcc8e17d071700ef81317a1b32eaa3991af72e08cae93e78865df519fe506
BuildRequires:  protobuf >= 2.6.0
BuildRequires:  protobuf-devel >= 2.6.0
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libstdc++
BuildRequires:  curl
BuildRequires:  make
BuildRequires:  unzip
Requires:       protobuf
Patch0:         CVE-2022-48468.patch

%description
Protocol Buffers (a.k.a., protobuf) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. You can find protobuf's documentation on the Google Developers site. This is the C implementation.

%package        devel
Summary:        Development files for protobuf
Group:          Development/Libraries
Requires:       protobuf-c = %{version}-%{release}

%description    devel
The protobuf-c-devel package contains libraries and header files for
developing applications that use protobuf-c.

%package        static
Summary:        protobuf-c static lib
Group:          Development/Libraries
Requires:       protobuf-c = %{version}-%{release}

%description    static
The protobuf-c-static package contains static protobuf-c libraries.

%prep
%autosetup -p1
autoreconf -iv

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
%{_libdir}/libprotobuf-c.a

%changelog
* Tue Oct 31 2023 Mukul Sikka <msikka@vmware.com> 1.3.1-3
- Fix for CVE-2022-48468
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.1-2
- Remove .la files
* Wed Sep 19 2018 Tapas Kundu <tkundu@vmware.com> 1.3.1-1
- Updated to release 1.3.1
* Thu Mar 30 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2.1-2
- Fix protobuf-c-static requires
* Sat Mar 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2.1-1
- Initial packaging for Photon
