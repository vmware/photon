%global srcname crash-gcore

Summary:    Gcore extension module for the crash utility
Name:       crash-gcore-command
Version:    1.6.3
Release:    1%{?dist}
License:    GPLv2
URL:        https://github.com/fujitsu/crash-gcore
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution: Photon

Source0: https://github.com/fujitsu/crash-gcore/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{srcname}=697952b7c55af5e4a7528cdd6fe616411d5147979fc90da55c0a3cee44510f39846e99bff3ac701c1ed98ee2c5d125e77c332b1f5b0be6e0ea1d98cf5d547a15

%ifarch aarch64
Patch0: gcore_defs.patch
%endif

BuildRequires: crash-devel

Requires: crash

Conflicts: crash < 8.0.2-5%{?dist}

%description
Command for creating a core dump file of a user-space task that was
running in a kernel dump file.

%prep
%autosetup -p1

%build
target="X86_64"

%ifarch aarch64
target="ARM64"
%endif

%make_build -f gcore.mk ARCH=SUPPORTED TARGET="${target}"

%install
install -m 0755 -d %{buildroot}%{_libdir}/crash/extensions

install -m 0755 -t %{buildroot}%{_libdir}/crash/extensions \
            %{_builddir}/%{name}-%{version}/gcore.so

%files
%defattr(-,root,root)
%license COPYING
%dir %{_libdir}/crash
%dir %{_libdir}/crash/extensions
%{_libdir}/crash/extensions/gcore.so

%changelog
* Mon Sep 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.6.3-1
- Move crash-gcore-command out of crash spec.
