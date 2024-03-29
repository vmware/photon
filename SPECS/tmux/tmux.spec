Summary:        Terminal multiplexer
Name:           tmux
Version:        3.3
Release:        3%{?dist}
License:        GPLv3+
URL:            https://tmux.github.io
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=2988ccef62337dee0a22579868608b611ce17e2160358a9ba4cc3a353fd1e6b1fea87584ceeed885f986b1786aac1b681c71bdf6a48ed4953809093280b38c09
Patch0:         tmux-CVE-2022-40716.patch

Requires:       libevent
Requires:       ncurses

BuildRequires:  libevent-devel
BuildRequires:  ncurses-devel

%description
Terminal multiplexer

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %dir %{_libdir}/debug
%{_datadir}/*
%exclude %dir %{_usrsrc}

%changelog
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 3.3-3
- Bump version as a part of ncurses upgrade to v6.4
* Wed Feb 01 2023 Harinadh D <hdommaraju@vmware.com> 3.3-2
- fix CVE-2022-40716
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 3.3-1
- Automatic Version Bump
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2-2
- Fix binary path
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2-1
- Automatic Version Bump
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1b-1
- Automatic Version Bump
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.7-1
- Updated to version 2.7.
* Tue May 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4-1
- Updated to version 2.4. Added make check.
* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
- Updated to version 2.3.
* Wed Jul 13 2016 Alexey Makhalov <amakhalov@vmware.com> 2.2-1
- Initial build.  First version
