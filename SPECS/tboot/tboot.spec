Summary:    Trusted pre-kernel module and tools.
Name:       tboot
Version:    1.9.6
Release:    1%{?dist}
License:    BSD
URL:        https://sourceforge.net/projects/tboot/
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    %{name}-%{version}.tar.gz
%define sha1 tboot=d060bf1ebd3e9d3d84ab39b78e0825b5f8489755
BuildRequires: trousers-devel
Requires:      libtspi
%description
Trusted Boot (tboot) is an open source, pre- kernel/VMM module that uses
Intel(R) Trusted Execution Technology (Intel(R) TXT) to perform a measured
and verified launch of an OS kernel/VMM.

%prep
%setup -q
%build
CFLAGS="%{optflags}"
export CFLAGS
make debug=y %{?_smp_mflags}

%install
make debug=y DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
/boot/*
/usr/*
%exclude %{_sysconfdir}

%changelog
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.9.6-1
-   Update to version 1.9.6 to get it to build with gcc 7.3
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.5-2
-   Ensure non empty debuginfo
*   Thu Mar 2 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.5-1
-   Initial build. First version
