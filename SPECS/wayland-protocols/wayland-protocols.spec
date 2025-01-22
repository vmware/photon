Summary:        Wayland protocols that adds functionality not available in the core protocol
Name:           wayland-protocols
Version:        1.25
Release:        2%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://wayland.freedesktop.org/

Source0:        http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
%define sha512  %{name}=8269694a0780e4d32f1982ff4cbb50b1ef85f08157b9486bc6d7e489c64665a9d9f959121d0eede7c7b108a604d974b64d74cfdef8b5f14304465309afb0768f

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  libffi-devel
BuildRequires:  wayland-devel
BuildRequires:  libwayland-client
BuildRequires:  libxml2-devel

%description
wayland-protocols contains Wayland protocols that adds functionality not
available in the Wayland core protocol. Such protocols either adds
completely new functionality, or extends the functionality of some other
protocol either in Wayland core, or some other protocol in
wayland-protocols.

%package devel
Summary:        Wayland protocols that adds functionality not available in the core protocol

%description devel
wayland-protocols contains Wayland protocols that adds functionality not
available in the Wayland core protocol. Such protocols either adds
completely new functionality, or extends the functionality of some other
protocol either in Wayland core, or some other protocol in
wayland-protocols.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
%meson_test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%license COPYING
%doc README.md
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/%{name}/

%changelog
*       Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.25-2
-       Bump version as a part of meson upgrade
*       Wed Jun 15 2022 Shivani Agarwal <shivania2@vmware.com> 1.25-1
-       Initial Version
