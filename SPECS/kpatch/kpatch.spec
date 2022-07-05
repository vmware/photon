Name:           kpatch
Summary:        Dynamic kernel patching
Version:        0.9.6
Release:        1%{?dist}
URL:            http://github.com/dynup/kpatch
License:        GPLv2
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/dynup/kpatch/archive/refs/tags/kpatch-v%{version}.tar.gz
%define sha512 kpatch=898c5704098c473187f2eab9bccd5fb3cfc31f4211492d658abcd0b7cac6d03f11a27df19a56ad17c20163803084ddf54a27defcf12b4975a8a8eb5dbad73f21

Patch0:         0001-Added-support-for-Photon-OS.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  elfutils
BuildRequires:  elfutils-devel
BuildRequires:  systemd-rpm-macros

Requires:       kmod
Requires:       bash
Requires:       rpm-build
Requires:	coreutils
Requires:	gawk

%description
Contains the kpatch utility, which allows loading of kernel livepatches.
kpatch is a Linux dynamic kernel patching tool which allows you to patch a
running kernel without rebooting or restarting any processes.  It enables
sysadmins to apply critical security patches to the kernel immediately, without
having to wait for long-running tasks to complete, users to log off, or
for scheduled reboot windows.  It gives more control over up-time without
sacrificing security or stability.

%package build
Requires: %{name} = %{version}-%{release}
Summary: Dynamic kernel patching

%description build
Contains the kpatch-build tool, to enable creation of kernel livepatches.

%package devel
Summary: Development files for kpatch

%description devel
Contains files for developing with kpatch.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
make install PREFIX=%{_usr} DESTDIR=%{buildroot} %{?_smp_mflags}

#%check
# make check require shellcheck package, which is not in photon

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_sbindir}/kpatch
%{_unitdir}/*
%{_sysconfdir}/init/kpatch.conf

%files build
%defattr(-,root,root,-)
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%doc README.md doc/patch-author-guide.md
%{_mandir}/man1/kpatch-build.1*
%{_mandir}/man1/kpatch.1*

%changelog
* Tue May 24 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-1
- Initial addition to photon. Modified from provided kpatch.spec on
- GitHub.
