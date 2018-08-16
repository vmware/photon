Summary:    Trusted pre-kernel module and tools.
Name:       tboot
Version:    1.9.5
Release:    3%{?dist}
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
/boot/%{name}.gz
/boot/%{name}-syms
%{_prefix}/sbin
%{_mandir}
%exclude %{_sysconfdir}

%files debuginfo
%defattr(-,root,root)
%{_libdir}/debug/usr/sbin/*
%{_prefix}/src/debug

%changelog
*   Thu Aug 16 2018 Ankit Jain <ankitja@vmware.com> 1.9.5-3
-   Resolved conflict while installing the package
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.5-2
-   Ensure non empty debuginfo
*   Thu Mar 2 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.5-1
-   Initial build. First version
