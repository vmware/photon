Summary:        Wayland protocols that adds functionality not available in the core protocol
Name:           wayland-protocols
Version:        1.31
Release:        4%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://wayland.freedesktop.org/

Source0:        https://gitlab.freedesktop.org/wayland/wayland-protocols/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

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

%package        devel
Summary:        Wayland protocols that adds functionality not available in the core protocol

%description    devel
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
*       Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.31-4
-       Bump version as a part of meson upgrade
*       Wed Dec 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 1.31-3
-       Release bump for SRP compliance
*       Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.31-2
-       Bump version as a part of libxml2 upgrade
*       Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 1.31-1
-       Automatic Version Bump
*       Tue Oct 25 2022 Gerrit Photon <photon-checkins@vmware.com> 1.27-1
-       Automatic Version Bump
*       Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.26-1
-       Automatic Version Bump
*       Wed Jun 15 2022 Shivani Agarwal <shivania2@vmware.com> 1.25-1
-       Initial Version
