Summary:    Trusted pre-kernel module and tools.
Name:       tboot
Version:    1.9.5
Release:    1%{?dist}
License:    BSD
URL:        https://sourceforge.net/projects/tboot/
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    %{name}-%{version}.tar.gz
%define sha1 tboot=fb5fe86278c003efa94ba5740d613cbff28de6e8
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
*   Thu Mar 2 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.5-1
-   Initial build. First version
