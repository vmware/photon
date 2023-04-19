Summary:        Wayland protocols that adds functionality not available in the core protocol
Name:           wayland-protocols
Version:        1.31
Release:        2%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://wayland.freedesktop.org/

Source0:        https://gitlab.freedesktop.org/wayland/wayland-protocols/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz
%define sha512  %{name}=402ce1915300e29afe554d77965ee0a28a5f22fdb5b901c4c640e59b9f3a9c11094e1edae87eea1e76eea557f6faf0c34a0c28ee7f6babb4dc3719329c4e25bf

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
*       Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.31-2
-       Bump version as a part of libxml2 upgrade
*       Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 1.31-1
-       Automatic Version Bump
*       Tue Oct 25 2022 Gerrit Photon <photon-checkins@vmware.com> 1.27-1
-       Automatic Version Bump
*       Thu Oct 06 2022 Gerrit Photon <photon-checkins@vmware.com> 1.26-1
-       Automatic Version Bump
*       Wed Jun 15 2022 Shivani Agarwal <shivania2@vmware.com> 1.25-1
-       Initial Version
