Summary:        A general purpose TCP-IP emulator
Name:           libslirp
Version:        4.7.0
Release:        3%{?dist}
URL:            https://gitlab.freedesktop.org/slirp/%{name}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://gitlab.com/qemu-project/libslirp/-/archive/v%{version}/%{name}-v%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: meson
BuildRequires: gcc
BuildRequires: glib-devel

Requires: glib

%description
A general purpose TCP-IP emulator used by virtual machine hypervisors
to provide virtual networking services.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel

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
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 4.7.0-2
- Release bump for SRP compliance
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.7.0-1
- Introduce libslirp. Needed for rootlesskit
