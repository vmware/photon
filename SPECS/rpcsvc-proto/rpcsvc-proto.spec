Summary:        rcpsvc protocol.x files and headers
Name:           rpcsvc-proto
Version:        1.4
Release:        1%{?dist}
Source0:        https://github.com/thkukuk/rpcsvc-proto/releases/download/v1.4/rpcsvc-proto-1.4.tar.gz
%define sha1    rpcsvc=01267dbc7d999c4ffdda1f69532e1f8331489b5f
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            https://github.com/thkukuk/rpcsvc-proto
Vendor:         VMware, Inc.
Distribution:   Photon

%description
The rpcsvc-proto package contains the rcpsvc protocol.x files and headers,
formerly included with glibc, that are not included in replacement
libtirpc-1.1.4, along with the rpcgen program.

%package    devel
Summary:    Development files for the rpcsvc library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description    devel
This package includes header files and libraries necessary for developing programs which use the rpcsvc library.

%prep
%setup -q

%build
autoreconf -fi
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%{_bindir}/rpcgen
%{_mandir}/man1/*

%files devel
%{_includedir}/rpcsvc/*

%changelog
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 1.4-1
- Initial version
