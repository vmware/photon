%global debug_package %{nil}
Summary:    Photon OS Installer
Name:       photon-os-installer
Version:    1.0
Release:    2%{?dist}
License:    Apache 2.0 and GPL 2.0
Group:      System Environment/Base
URL:        https://github.com/vmware/photon-os-installer
Source0:    %{name}-%{version}.tar.gz
Patch0:     support_insecure_installation.patch
Vendor:     VMware, Inc.
Distribution:   Photon
%define sha1 %{name}=cc86d22b7ef8495164fec1fb7d96bb97a2fb82c6
BuildRequires: python3-devel
BuildRequires: python3-pyinstaller
BuildRequires: python3-requests
BuildRequires: python3-cracklib
BuildRequires: python3-curses
Requires:      zlib
Requires:      glibc

%description
This is to create rpm for installer code

%prep
%setup -n %{name}-%{version}
%patch0 -p1

%build
pyinstaller --onefile photon-installer.spec

%install
mkdir -p %{buildroot}%{_bindir}
cp dist/photon-installer %{buildroot}%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/photon-installer

%changelog
*   Wed Dec 16 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.0-2
-   Add support for insecure_installation so that rpms can be
-   served from untrusted https url
*   Thu Aug 06 2020 Piyush Gupta <gpiyush@vmware.com> 1.0-1
-   Initial photon installer for Photon OS.
