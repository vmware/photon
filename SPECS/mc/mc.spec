Summary:        File manager
Name:           mc
Version:        4.8.28
Release:        2%{?dist}
License:        GPLv3+
URL:            https://www.midnight-commander.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.midnight-commander.orgtar/%{name}-%{version}.tar.xz
%define sha512  %{name}=ca3b3a57281e9387cb52bf1fcfc3f39a4d5f438aafc256dc492c192678824f67c983a852c759664efc5bc6d0de471c9b3929834f8301f6302ca1ebeee513fdfd

Requires:       glib
Requires:       pcre
Requires:       slang

BuildRequires:  glib-devel
BuildRequires:  pcre-devel
BuildRequires:  slang-devel

%description
MC (Midnight Commander) is a text-mode full-screen file manager and visual shell.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check
%endif

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/*
%exclude %dir %{_usrsrc}
%exclude %dir %{_libdir}

%changelog
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.8.28-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 4.8.28-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 4.8.26-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 4.8.25-1
- Automatic Version Bump
* Thu Sep 06 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.8.21-1
- Update to version 4.8.21
* Fri Aug 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.8.19-2
- Disable extfs test
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.8.19-1
- Update package version
* Tue Jul 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.17-1
- Initial build. First version
