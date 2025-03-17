Summary:    The mdadm program controls Linux md devices (software RAID arrays)
Name:       mdadm
Version:    4.4
Release:    1%{?dist}
URL:        https://git.kernel.org/pub/scm/utils/mdadm/mdadm.git/about
Group:      Applications/Utilities
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://www.kernel.org/pub/linux/utils/raid/mdadm/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: build-fix.patch

BuildRequires: systemd-devel

%description
The mdadm program is used to create, manage, and monitor Linux MD (software
RAID) devices.  As such, it provides similar functionality to the raidtools
package.  However, mdadm is a single program, and it can perform
almost all functions without a configuration file, though a configuration
file can be used to help with some common tasks.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install %{?_smp_mflags} \
  BINDIR=%{_sbindir} \
  SYSTEMD_DIR=%{_unitdir} \
  install-systemd

install -Dp -m 644 documentation/mdadm.conf-example \
    %{buildroot}%{_sysconfdir}/%{name}.conf

mkdir -p -m 755 %{buildroot}%{_datadir}/%{name}
install -Dp -m 755 misc/mdcheck %{buildroot}%{_datadir}/%{name}/mdcheck

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_udevrulesdir}/*-md-*
%{_sbindir}/%{name}
%{_sbindir}/mdmon
%{_unitdir}/md*
%{_mandir}/man*/md*
%{_libdir}/systemd/system-shutdown/mdadm.shutdown
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*

%changelog
* Wed Feb 19 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.4-1
- Initial version.
