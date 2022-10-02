Summary:     Linux Containers File System
Name:        lxcfs
Version:     4.0.6
Release:     2%{?dist}
URL:         https://linuxcontainers.org/lxcfs/downloads/
Source0:     %{name}-%{version}.tar.gz
License:     LGPL 2.1+
Group:       System Environment/Libraries
%define sha512 %{name}=843ca196304efc963549c0e081bea4d58182887611da36232e875de4898d738111a967d89b4b49a9df51f25daf119ad2d488b8298cdef82926be03a7fa99a8a2
Vendor:      VMware, Inc.
Distribution:  Photon
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
make install DESTDIR=%{buildroot} %{?_smp_mflags}
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
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.0.6-2
- Remove .la files
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.6-1
- Automatic Version Bump
* Wed Apr 22 2020 Anish Swaminathan <anishs@vmware.com>  4.0.3-1
- Initial release.
