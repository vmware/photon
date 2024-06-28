Summary:        rcpsvc protocol.x files and headers
Name:           rpcsvc-proto
Version:        1.4.3
Release:        1%{?dist}
Source0:        https://github.com/thkukuk/rpcsvc-proto/releases/download/v1.4/%{name}-%{version}.tar.xz
%define sha512  rpcsvc=e46ba9ccdd6c520128bf3a154db90742f288a4d593b094a630141cdc5aeb834ffebf9b0eb6d5d0aad9faef3c445c75e2355cbc3e1382b50d29f4d2799441c6e9
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            https://github.com/thkukuk/rpcsvc-proto
Vendor:         VMware, Inc.
Distribution:   Photon
%define BuildRequiresNative rpcsvc-proto

%description
The rpcsvc-proto package contains the rcpsvc protocol.x files and headers,
formerly included with glibc, that are not included in replacement
libtirpc-1.1.4, along with the rpcgen program.

%package        devel
Summary:        Development files for the rpcsvc library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package includes header files and libraries necessary for developing programs which use the rpcsvc library.

%prep
%autosetup

%build
if [ %{_host} != %{_build} ]; then
  # use native rpcgen
  sed -i 's#$(top_builddir)/rpcgen/##' rpcsvc/Makefile.am
fi
autoreconf -fi

%configure
make %{?_smp_mflags}

%install
make install %{?_smp_mflags} DESTDIR=%{buildroot}

%files
%{_bindir}/rpcgen
%{_mandir}/man1/*

%files devel
%{_includedir}/rpcsvc/*

%changelog
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.4.3-1
- Automatic Version Bump
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.2-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.4-2
- Cross compilation support
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 1.4-1
- Initial version.
