Summary:        Wayland protocols that adds functionality not available in the core protocol
Name:           wayland-protocols
Version:        1.27
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://wayland.freedesktop.org/

Source0:        https://gitlab.freedesktop.org/wayland/wayland-protocols/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz
%define sha512  %{name}=c0a49bc46c663c9f602998dfe2e184c09756790fbcc7acbc2bf9d9cf8f7d6dcdd00259b768222a30e5d134e6f97f7f4faf252947b544e8b32f53278b70da0390

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
*       Tue Oct 25 2022 Gerrit Photon <photon-checkins@vmware.com> 1.27-1
-       Automatic Version Bump
*       Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.26-1
-       Automatic Version Bump
*       Wed Jun 15 2022 Shivani Agarwal <shivania2@vmware.com> 1.25-1
-       Initial Version
