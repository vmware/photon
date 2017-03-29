Summary:       Linux Virtual Server administration
Name:          ipvsadm
Version:       1.29
Release:       1%{?dist}
License:       GPLv2
URL:           http://www.kernel.org/
Group:         System Environment/tools
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://www.kernel.org/pub/linux/utils/kernel/ipvsadm/%{name}-%{version}.tar.xz
%define sha1 ipvsadm=d51539fd23f19cf12e1c4d5611dd1050e5d3046a
BuildRequires: which popt-devel libnl-devel
Requires:      popt libnl
%description
Ipvsadm is  used  to set up, maintain or inspect the virtual server table in
the Linux kernel.

%prep
%setup -q

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
*   Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.29-1
-   Upgrading to version 1.29
*   Fri Nov 11 2016 Alexey Makhalov <amakhalov@vmware.com> 1.28-1
-   Initial build. First version
