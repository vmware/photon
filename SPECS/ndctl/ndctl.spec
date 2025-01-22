Summary:        Manage "libnvdimm" subsystem devices (Non-volatile Memory)
Name:           ndctl
Version:        74
Release:        3%{?dist}
Group:          System Environment/Base
Url:            https://github.com/pmem/ndctl
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pmem/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=b8c4f8ee39aeb85679a97c46cb1ec345041ad91074be35f04de3a688957164374f92b3efc4f745c3b28098086689db861fd22799b056230267b3327406749473

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  meson
BuildRequires:  asciidoc3
BuildRequires:  which
BuildRequires:  xmlto
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  kmod-devel
BuildRequires:  systemd-devel
BuildRequires:  json-c-devel
BuildRequires:  keyutils-devel
BuildRequires:  iniparser-devel
BuildRequires:  systemd-rpm-macros

%description
Utility library for managing the "libnvdimm" subsystem.  The "libnvdimm"
subsystem defines a kernel device model and control message interface for
platform NVDIMM resources.

%package        devel
Summary:        Development files for ndctl
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n     daxctl
Summary:        Manage Device-DAX instances
Group:          System Environment/Base

%description -n daxctl
The daxctl utility provides enumeration and provisioning commands for
the Linux kernel Device-DAX facility. This facility enables DAX mappings
of performance / feature differentiated memory without need of a
filesystem.

%package -n     daxctl-devel
Summary:        Development files for daxctl
Group:          Development/Libraries
Requires:       daxctl = %{version}-%{release}

%description -n daxctl-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}, a library for enumerating
"Device DAX" devices.  Device DAX is a facility for establishing DAX
mappings of performance / feature-differentiated memory.

%package -n cxl
Summary:        Manage CXL devices

%description -n cxl
The cxl utility provides enumeration and provisioning commands for
the Linux kernel CXL devices.

%package -n cxl-devel
Summary:        Development files for libcxl
Requires:       cxl = %{version}-%{release}

%description -n cxl-devel
This package contains libraries and header files for developing applications
that use libcxl, a library for enumerating and communicating with CXL devices.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%meson \
    -Ddocs=disabled

%meson_build

%install
%meson_install

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libdir}/libndctl.so.*
%{_unitdir}/%{name}-monitor.service
%{_sysconfdir}/modprobe.d/nvdimm-security.conf
%{_sysconfdir}/%{name}/keys/keys.readme
%dir %{_sysconfdir}/ndctl.conf.d
%config(noreplace) %{_sysconfdir}/ndctl.conf.d/monitor.conf
%config(noreplace) %{_sysconfdir}/ndctl.conf.d/ndctl.conf
%{_datadir}/bash-completion/completions/ndctl

%files devel
%defattr(-,root,root)
%license COPYING
%{_includedir}/%{name}/
%{_libdir}/libndctl.so
%{_libdir}/pkgconfig/libndctl.pc

%files -n daxctl
%defattr(-,root,root)
%{_bindir}/daxctl
%{_libdir}/libdaxctl.so.*
%{_datadir}/daxctl/daxctl.conf
%{_datadir}/bash-completion/completions/daxctl
%config(noreplace) %{_sysconfdir}/daxctl.conf.d/daxctl.example.conf
%{_unitdir}/daxdev-reconfigure@.service
%config %{_udevrulesdir}/90-daxctl-device.rules

%files -n daxctl-devel
%defattr(-,root,root)
%license COPYING
%{_includedir}/daxctl/
%{_libdir}/libdaxctl.so
%{_libdir}/pkgconfig/libdaxctl.pc

%files -n cxl
%defattr(-,root,root)
%{_libdir}/libcxl.so.*
%{_bindir}/cxl
%{_datadir}/bash-completion/completions/cxl

%files -n cxl-devel
%defattr(-,root,root)
%{_includedir}/cxl/
%{_libdir}/libcxl.so
%{_libdir}/pkgconfig/libcxl.pc

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 74-3
- Bump version as a part of meson upgrade
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 74-2
- Release bump for SRP compliance
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 74-1
- Automatic Version Bump
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 73-1
- Upgrade to v73
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 71-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 69-1
- Automatic Version Bump
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 62-2
- Use asciidoc3
* Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 62-1
- Upgrade to v62
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 56-3
- Add kmod-devel to BuildRequires
* Mon Apr 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 56-2
- Removing the Requires section
* Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 56-1
- Initial build.  First version
