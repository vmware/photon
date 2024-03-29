Summary:        SELinux policy core utilities
Name:           selinux-python
Version:        3.5
Release:        2%{?dist}
License:        Public Domain
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=2ac176a9f078f2b2721e5871ba21e92041eed54fc692fd8d809ff14327beee6de63b3084d0f1053a640b9e40bcc6461498915bb9b038a658cd772f77d80fd217

BuildRequires:  python3-devel
BuildRequires:  libsepol-devel
BuildRequires:  libselinux-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip

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
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_mandir}/ru
%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{python3_sitelib}/*
%{_datadir}/bash-completion/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%exclude %{_sharedstatedir}/sepolgen/perm_map

%changelog
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.5-2
- Fix requires
* Wed Apr 05 2023 Gerrit Photon <photon-checkins@vmware.com> 3.5-1
- Automatic Version Bump
* Sun Aug 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.4-1
- Upgrade v3.4
* Fri Jul 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-3
- Add python3-audit to Requires
* Thu Jul 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-2
- Fix Requires
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Initial version.
