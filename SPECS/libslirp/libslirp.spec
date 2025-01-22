Summary:        A general purpose TCP-IP emulator
Name:           libslirp
Version:        4.7.0
Release:        3%{?dist}
License:        BSD and MIT
URL:            https://gitlab.freedesktop.org/slirp/%{name}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://gitlab.com/qemu-project/libslirp/-/archive/v%{version}/%{name}-v%{version}.tar.gz
%define sha512  %{name}-v%{version}=387f4a6dad240ce633df2640bb49c6cb0041c8b3afc8d0ef38186d385f00dd9e4ef4443e93e1b71dbf05e22892b6f2771a87a202e815d8ec899ab5c147a1f09f

BuildRequires: meson
BuildRequires: gcc
BuildRequires: glib-devel >= 2.68.4

Requires: glib >= 2.68.4

%description
A general purpose TCP-IP emulator used by virtual machine hypervisors
to provide virtual networking services.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel >= 2.68.4

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
%meson
%meson_build

%install
%meson_install

%check
%if 0%{?with_check}
./%{_arch}-vmware-linux/pingtest
%endif

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYRIGHT
%doc README.md CHANGELOG.md
%{_libdir}/%{name}.so*

%files devel
%dir %{_includedir}/slirp/
%{_includedir}/slirp/*
%{_libdir}/pkgconfig/slirp.pc

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 4.7.0-3
- Bump version as a part of meson upgrade
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.7.0-2
- Bump version as part of glib upgrade
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.7.0-1
- Introduce libslirp. Needed for rootlesskit
