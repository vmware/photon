Name:           dbus-broker
Version:        33
Release:        2%{?dist}
Summary:        Linux D-Bus Message Broker
License:        ASL 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security
URL:            https://github.com/bus1/dbus-broker

Source0: https://github.com/bus1/dbus-broker/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=776684a5d19a6c25fc46dff19821014a32d967f8132385b86c5281f2d69192dce64b3ad92ae6a158d1d64753e89d918385a1a31f32811f54060504113f065baa

Source1: %{name}.sysusers

Provides:       bundled(c-dvar) = 1
Provides:       bundled(c-ini) = 1
Provides:       bundled(c-list) = 3
Provides:       bundled(c-rbtree) = 3
Provides:       bundled(c-shquote) = 1

BuildRequires:  expat-devel
BuildRequires:  libcap-ng
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3-docutils
BuildRequires:  systemd-devel
BuildRequires:  audit-devel
BuildRequires:  libcap-ng-devel

Requires: systemd

%description
dbus-broker is an implementation of a message bus as defined by the D-Bus
specification. Its aim is to provide high performance and reliability, while
keeping compatibility to the D-Bus reference implementation. It is exclusively
written for Linux systems, and makes use of many modern features provided by
recent Linux kernel releases.

%prep
%autosetup -p1

%build
%{meson} \
    --prefix=%{_usr} \
    -Dselinux=true \
    -Daudit=true

%{meson_build}

%install
%{meson_install}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%check
%{meson_test}

%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post %{name}.service
%systemd_user_post %{name}.service
%journal_catalog_update

%preun
%systemd_preun %{name}.service
%systemd_user_preun %{name}.service

%postun
%systemd_postun %{name}.service
%systemd_user_postun %{name}.service

%triggerpostun -- dbus
if [ $2 -eq 0 ] && [ -x %{_bindir}/systemctl ]; then
  # The `dbus-daemon` package used to provide the default D-Bus
  # implementation. We continue to make sure that if you uninstall it, we
  # re-evaluate whether to enable dbus-broker to replace it. If we don't,
  # you might end up without any bus implementation active.
  systemctl --no-reload          preset dbus-broker.service || :
  systemctl --no-reload --global preset dbus-broker.service || :
fi

%files
%license AUTHORS
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-launch
%{_journalcatalogdir}/%{name}.catalog
%{_journalcatalogdir}/%{name}-launch.catalog
%{_unitdir}/%{name}.service
%{_userunitdir}/%{name}.service
%{_sysusersdir}/%{name}.sysusers

%changelog
* Wed Sep 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 33-2
- Fix spec issues
- Create dbus user
* Thu Feb 16 2023 Susant Sahani <ssahani@vmware.com> 33-1
- Update version
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 32-2
- Update release to compile with python 3.11
* Tue Aug 30 2022 Susant Sahani <ssahani@vmware.com> 32-1
- Update version
* Thu May 26 2022 Susant Sahani <ssahani@vmware.com> 31-1
- Update version
* Wed Jul 14 2021 Susant Sahani <ssahani@vmware.com> 29-1
- Update version and switch to meson
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
