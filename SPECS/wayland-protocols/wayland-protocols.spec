Summary:        Wayland protocols that adds functionality not available in the core protocol
Name:           wayland-protocols
Version:        1.26
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://wayland.freedesktop.org/

Source0:        http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
%define sha512  %{name}=fa9c3963b548197461c8c0b9e16ebbf9cfa5b60053fc17f51b41e63a55b8c5420dd7e42313f93946b438ab47f04e1cd17bc92aae9e1074b47177dc7ce7042167

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
*       Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.26-1
-       Automatic Version Bump
*       Wed Jun 15 2022 Shivani Agarwal <shivania2@vmware.com> 1.25-1
-       Initial Version
