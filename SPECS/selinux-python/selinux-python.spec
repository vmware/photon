Summary:        SELinux policy core utilities
Name:           selinux-python
Version:        3.3
Release:        4%{?dist}
License:        Public Domain
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=a69948a8b139a309f18632440e4204f49832a94b8b6be50e162d3dacb16698effeb1a77c44462e8cc7dc3dd600b887b9ab2fef618c31d3e0fe0de216a6aaebe3

BuildRequires:  python3-devel
BuildRequires:  libsepol-devel
BuildRequires:  libselinux-devel

Requires: python3
Requires: libsemanage-python3 = %{version}
Requires: libselinux-python3 = %{version}
Requires: libsepol = %{version}
Requires: libselinux = %{version}
Requires: python3-audit
Requires: setools
Requires: python3-distro
Requires: python3-networkx

%description
The %{name} package contains the management tools use to manage an SELinux environment.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install

rm -rf %{buildroot}%{_mandir}/ru

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{python3_sitelib}/*
%{_datadir}/bash-completion/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%exclude %{_sharedstatedir}/sepolgen/perm_map

%changelog
* Tue Jan 02 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.3-4
- Fix requires
* Fri Jul 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-3
- Add python3-audit to Requires
* Thu Jul 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-2
- Fix Requires
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Initial version.
