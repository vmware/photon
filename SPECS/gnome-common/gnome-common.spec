Summary:        Common development macros for GNOME
Name:           gnome-common
Version:        3.18.0
Release:        5%{?dist}
URL:            https://www.gnome.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{version}/%{name}-%{version}.tar.xz
%define sha512 gnome-common=b931c9a6668d996560549738bb2d95f86f56fa68ce930c077275bdc8fddbc2d28d215c1190099db1df851417902fca87ec81f1c0e644c5b9630a175e1cde0719

Source1: license.txt
%include %{SOURCE1}
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

%description
This provides Common development macros for GNOME.

%prep
%autosetup
./autogen.sh

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
# Rename the conflicting files to avoid install time conflicts with
# autoconf-archive package
%{__mv} %{buildroot}%{_datadir}/aclocal/ax_check_enable_debug.m4 \
  %{buildroot}%{_datadir}/aclocal/ax_check_enable_debug_%{name}.m4
%{__mv} %{buildroot}%{_datadir}/aclocal/ax_code_coverage.m4 \
  %{buildroot}%{_datadir}/aclocal/ax_code_coverage_%{name}.m4

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/gnome-autogen.sh
%{_datadir}/aclocal/*.m4

%changelog
*   Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.18.0-5
-   Release bump for SRP compliance
*   Fri Jan 22 2021 Dweep Advani <dadvani@vmware.com> 3.18.0-4
-   Fix install time conflicts with autoconf-archive
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.18.0-3
-   Fix arch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.18.0-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  3.18.0-1
-   Upgrade to 3.18.0
*   Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.14.0-1
-   Add gnome-common v3.14.0
