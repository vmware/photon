Summary:       Linux Virtual Server administration
Name:          ipvsadm
Version:       1.31
Release:       1%{?dist}
License:       GPLv2
URL:           http://www.kernel.org/
Group:         System Environment/tools
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://www.kernel.org/pub/linux/utils/kernel/ipvsadm/%{name}-%{version}.tar.xz
%define sha1 ipvsadm=ddb62a54944f3067f2b94a7e4de8c7b29cf535fb
BuildRequires: which popt-devel libnl-devel
Requires:      popt libnl
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
%autosetup

%build
make

%install
make install BUILD_ROOT=%{buildroot} MANDIR=%{_mandir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/*
/sbin/*
%{_mandir}/*

%changelog
*   Thu May 14 2020 Susant Sahani <ssahani@vmware.com> 1.31-1
-   Update to version 1.31
*   Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.29-1
-   Upgrading to version 1.29
*   Fri Nov 11 2016 Alexey Makhalov <amakhalov@vmware.com> 1.28-1
-   Initial build. First version
