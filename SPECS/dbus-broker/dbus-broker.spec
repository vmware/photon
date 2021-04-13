Name:           dbus-broker
Version:        28
Release:        1%{?dist}
Summary:        Linux D-Bus Message Broker
License:        ASL 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security

URL:            https://github.com/bus1/dbus-broker
Source0:        https://github.com/bus1/dbus-broker/releases/download/v%{version}/dbus-broker-%{version}.tar.xz
%define sha1    dbus-broker=2602b87b336875bc1fd6866004f16013e6cf3fe4

Provides:       bundled(c-dvar) = 1
Provides:       bundled(c-ini) = 1
Provides:       bundled(c-list) = 3
Provides:       bundled(c-rbtree) = 3
Provides:       bundled(c-shquote) = 1

BuildRequires:  expat-devel
BuildRequires:  libcap-ng
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3-docutils
BuildRequires:  systemd
BuildRequires:  systemd-devel

%description
dbus-broker is an implementation of a message bus as defined by the D-Bus
specification. Its aim is to provide high performance and reliability, while
keeping compatibility to the D-Bus reference implementation. It is exclusively
written for Linux systems, and makes use of many modern features provided by
recent Linux kernel releases.

%prep
%setup -n %{name}-%{version}

%build
CONFIGURE_OPTS=(
   --prefix=/usr
)
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

meson build ${CONFIGURE_OPTS[@]}
ninja -C build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
DESTDIR=%{buildroot} ninja -C build install

%check
%meson_test

%post

if [ $1 -eq 1 ] ; then
        systemctl --no-reload          disable dbus-daemon.service &>/dev/null || :
        systemctl --no-reload --global disable dbus-daemon.service &>/dev/null || :
        systemctl --no-reload          enable dbus-broker.service &>/dev/null || :
        systemctl --no-reload --global enable dbus-broker.service &>/dev/null || :
fi

%journal_catalog_update

%preun
%systemd_preun dbus-broker.service
%systemd_user_preun dbus-broker.service

%postun
%systemd_postun dbus-broker.service
%systemd_user_postun dbus-broker.service

%files
%license AUTHORS
%license LICENSE
%{_bindir}/dbus-broker
%{_bindir}/dbus-broker-launch
%{_journalcatalogdir}/dbus-broker.catalog
%{_journalcatalogdir}/dbus-broker-launch.catalog
%{_unitdir}/dbus-broker.service
%{_userunitdir}/dbus-broker.service

%changelog
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 28-1
- Automatic Version Bump
* Sat Jan 23 2021 Susant Sahani <ssahani@vmware.com> 26-1
- Update version
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 24-1
- Automatic Version Bump
* Fri Aug 14 2020 Susant Sahani <ssahani@vmware.com> 23-1
- Update to v23
* Tue May 05 2020 Susant Sahani <ssahani@vmware.com> 22-1
- Initial RPM release
