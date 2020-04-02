%global _vpath_srcdir .
%global _vpath_builddir %{_target_platform}
%global __global_cflags  %{optflags}
%global __global_cxxflags  %{optflags}
%global __global_ldflags -Wl,-z,relro

Name:           dbus-broker
Version:        22
Release:        1%{?dist}
Summary:        Linux D-Bus Message Broker
License:        ASL 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security

URL:            https://github.com/bus1/dbus-broker
Source0:        https://github.com/bus1/dbus-broker/releases/download/v%{version}/dbus-broker-%{version}.tar.xz
%define sha1    dbus-broker=b0e3b4c33712ee8476faf550939f3a032327fafb

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
)

%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install

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
* Wed May 05 2020 Susant Sahani <ssahani@vmware.com> 22-1
- Initial RPM release
