%define maj_ver       4.5
%define extra_version 0.20

Name:           perftest
Summary:        IB Performance tests
Version:        4.5.0.20
Release:        1%{?dist}
License:        GPLv2 or BSD
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/linux-rdma/perftest

Source0: https://github.com/linux-rdma/perftest/releases/download/v%{version}-%{extra_version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=ae9c722516909b63ac00b3fe19750ed603651c875ad73702ab39e558c4b9da910deba891a27c82d02c9cd20b27c9ccadd8f463a153e7a634e91ee399c89d6c37

BuildRequires:  rdma-core-devel
BuildRequires:  pciutils-devel
BuildRequires:  build-essential

Requires:       rdma-core
Requires:       libibverbs
Requires:       libibverbs-utils
Requires:       libibumad
Requires:       pciutils
Requires:       librdmacm

%description
This is a collection of tests written over uverbs intended for use as a
performance micro-benchmark. The tests may be used for HW or SW tuning
as well as for functional testing.

%package doc
Summary:    Documentation
Requires:   %{name} = %{version}-%{release}

%description doc
Documentation & man pages

%prep
%autosetup -p1 -n %{name}-%{maj_ver}-%{extra_version}

%build
sh ./autogen.sh
%configure
%make_build
chmod -x runme

%install
%make_install %{_smp_mflags}

%if 0%{?with_check}
%check
make check %{_smp_mflags}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%_bindir/*

%files doc
%defattr(-,root,root)
%doc runme
%_mandir/man1/*.1*

%changelog
* Thu Feb 16 2023 Harinadh D <hdommaraju@vmware.com> 4.5.0.20-1
- Initial release
