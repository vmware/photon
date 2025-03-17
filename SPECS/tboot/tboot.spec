Summary:    Trusted pre-kernel module and tools.
Name:       tboot
Version:    1.10.5
Release:    2%{?dist}
URL:        https://sourceforge.net/projects/tboot/
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildArch:     x86_64
BuildRequires: trousers-devel
Requires:      libtspi
%description
Trusted Boot (tboot) is an open source, pre- kernel/VMM module that uses
Intel(R) Trusted Execution Technology (Intel(R) TXT) to perform a measured
and verified launch of an OS kernel/VMM.

%prep
%autosetup
%build
export CFLAGS
make debug=y %{?_smp_mflags}

%install
make debug=y DESTDIR=%{buildroot} install %{?_smp_mflags}

%files
%defattr(-,root,root)
/boot/%{name}.gz
/boot/%{name}-syms
%{_prefix}/sbin
%{_mandir}
%exclude %{_sysconfdir}

%changelog
*   Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.10.5-2
-   Release bump for SRP compliance
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.10.5-1
-   Automatic Version Bump
*   Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.9.12-2
-   Bump up release for openssl
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.12-1
-   Automatic Version Bump
*   Fri Dec 14 2018 Ankit Jain <ankitja@vmware.com> 1.9.7-3
-   Resolved conflict while installing the package
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.9.7-2
-   Adding BuildArch
*   Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.9.7-1
-   Update to version 1.9.7.
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.9.6-1
-   Update to version 1.9.6 to get it to build with gcc 7.3
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.5-2
-   Ensure non empty debuginfo
*   Thu Mar 2 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.5-1
-   Initial build. First version
