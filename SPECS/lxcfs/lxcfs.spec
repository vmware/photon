Summary:     Linux Containers File System
Name:        lxcfs
Version:     4.0.5
Release:     2%{?dist}
URL:         https://linuxcontainers.org/lxcfs/downloads/
License:     LGPL 2.1+
Group:       System Environment/Libraries
Vendor:		 VMware, Inc.
Distribution:  Photon

Source0:     %{name}-%{version}.tar.gz
%define sha512 %{name}=6961d7cb08a7562a17e513b53b1a3a75993824b1e1a4de12d080e73ba86f9883abb43b039ce82e938d3f2e9fffa7eea6bb1a12b07b9b281e393946146a9e3a86

BuildRequires: gcc
BuildRequires: libtool
BuildRequires: fuse-devel
BuildRequires: systemd

Requires:      fuse

%description
LXCFS is a simple userspace filesystem designed to work around some current limitations of the Linux kernel.

%prep
%autosetup -p1

%build
%configure \
	--with-init-script=systemd
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

%post
%systemd_post lxcfs.service

%preun
%systemd_preun lxcfs.service

%postun
%systemd_postun lxcfs.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_sharedstatedir}/%{name}
/lib/systemd/system/%{name}.service
%{_bindir}/lxcfs
%config(noreplace) %{_datarootdir}/lxc/config/common.conf.d/00-%{name}.conf
%{_datarootdir}/%{name}/lxc.mount.hook
%{_datarootdir}/%{name}/lxc.reboot.hook
%{_libdir}/%{name}/liblxcfs.so

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.0.5-2
- Remove .la files
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.5-1
- Automatic Version Bump
* Wed Apr 22 2020 Anish Swaminathan <anishs@vmware.com>  4.0.3-1
- Initial release.
