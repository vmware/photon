%global debug_package %{nil}

Name:           abupdate
Summary:        A/B partition set update and rollback
Version:        1.0
Release:        3%{?dist}
License:        GPLv2
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

Source0:        abupdate
Source1:        abupdate.conf
Source2:        abupdate.service
Source3:        README

BuildRequires:  systemd-rpm-macros

Requires:       bash
Requires:       systemd
Requires:       kexec-tools
Requires:       util-linux
Requires:       rsync
Requires:       grub2
Requires:       tar

# Also requires grub2-pc if BIOS, efibootmgr if UEFI
# That will have to be installed by the user based on their system
Recommends:     grub2-pc
Recommends:     efibootmgr

%description
Contains the abupdate utility, which provides capabilities in conjunction with an A/B set of partitions,
to atomically update packages/kernel versions, and safely rollback if something goes wrong.
abupdate has the ability to mirror data and update packages/kernel between partition sets,
as well as switch between sets, and rollback from A to B.

%install
mkdir -p %{buildroot}{%{_sbindir},%{_sysconfdir},%{_unitdir},%{_docdir}}
cp %{SOURCE0} %{buildroot}%{_sbindir}
cp %{SOURCE1} %{buildroot}%{_sysconfdir}
cp %{SOURCE2} %{buildroot}%{_unitdir}
cp %{SOURCE3} %{buildroot}%{_docdir}

%files
%defattr(-,root,root,-)
%doc %{_docdir}/README
%{_sbindir}/abupdate
%config(noreplace) %{_sysconfdir}/abupdate.conf
%{_unitdir}/abupdate.service

%changelog
* Thu Feb 23 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 1.0-3
- Enable kexec for ARM, don't replace abupdate.conf. Edit abupdate
- to support aarch64.
* Thu Feb 23 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0-2
- Requires kexec-tools only in x86_64
* Thu Oct 20 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 1.0-1
- Initial addition to Photon.
