%define extra_version 0.11
Name:           perftest
Summary:        IB Performance tests
Version:        4.4
Release:        1%{?dist}
License:        GPLv2 or BSD
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         https://github.com/linux-rdma/perftest/releases/download/v%{version}-%{extra_version}/%{name}-%{version}-%{extra_version}.tar.gz
%define sha1    perftest=be0719d68f25927daded12d29ff08ff4a5247170
URL:            https://github.com/linux-rdma/perftest
BuildRequires:  rdma-core
BuildRequires:  rdma-core-devel
BuildRequires:  libibverbs
BuildRequires:  librdmacm
BuildRequires:  libibumad
BuildRequires:  pciutils-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
Requires:       rdma-core
Requires:       libibverbs
Requires:       librdmacm
Requires:       libibumad

%description
This is a collection of tests written over uverbs intended for use as a
performance micro-benchmark. The tests may be used for HW or SW tuning
as well as for functional testing.

%prep
%autosetup -n %{name}-%{version}-%{extra_version}

%build
sed -i 's/^struct perftest_parameters/extern struct perftest_parameters/' ./src/raw_ethernet_resources.c
autoreconf -fi
%configure
%{__make}
chmod -x runme

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README COPYING runme
%_bindir/*

%changelog
* Thu Apr 08 2021 Harinadh D <hdommaraju@vmware.com> 4.4-1
- Initial release
