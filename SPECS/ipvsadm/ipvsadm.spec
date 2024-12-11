Summary:       Linux Virtual Server administration
Name:          ipvsadm
Version:       1.31
Release:       3%{?dist}
URL:           http://www.kernel.org/
Group:         System Environment/tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       https://www.kernel.org/pub/linux/utils/kernel/ipvsadm/%{name}-%{version}.tar.xz
%define sha512  %{name}=1c7187405771e702eff0009d688fa697375b833a486ff88b41a4a0dcfaa3e9884c7e3bc34375efea5f6a2d025847c9fac9fd6ba694ec3bf2fc9d357eef2cb631

Source1: license.txt
%include %{SOURCE1}

BuildRequires: which
BuildRequires: popt-devel
BuildRequires: libnl-devel

Requires:      popt
Requires:      libnl

%description
ipvsadm is used to setup, maintain, and inspect the virtual server
table in the Linux kernel. The Linux Virtual Server can be used to
build scalable network services based on a cluster of two or more
nodes. The active node of the cluster redirects service requests to a
collection of server hosts that will actually perform the
services.

Supported Features include:
two protocols (TCP and UDP), three packet-forwarding methods
(NAT, tunneling, and direct routing), and eight load balancing algorithms
(round robin  weighted round robin, least-connection, weighted least-connection,
locality-based least-connection, locality-based least-connection with replication,
destination-hashing, and source-hashing).

%prep
%autosetup -p1

%build
# make doesn't support _smp_mflags
make

%install
# make doesn't support _smp_mflags
make install BUILD_ROOT=%{buildroot} MANDIR=%{_mandir} SBIN=%{buildroot}%{_sbindir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
%{_mandir}/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.31-3
- Release bump for SRP compliance
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.31-2
- Fix binary path
* Thu May 14 2020 Susant Sahani <ssahani@vmware.com> 1.31-1
- Update to version 1.31
* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.29-1
- Upgrading to version 1.29
* Fri Nov 11 2016 Alexey Makhalov <amakhalov@vmware.com> 1.28-1
- Initial build. First version
