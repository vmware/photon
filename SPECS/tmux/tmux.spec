Summary:        Terminal multiplexer
Name:           tmux
Version:        3.1b
Release:        4%{?dist}
License:        GPLv3+
URL:            https://tmux.github.io
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=29fd56715746bd748036ca71195bc15ae5b663ac4944cf2da07a72fe3c7c881a1f27f32406cde4852e7f76b77cb2eadb5184b2b644b11d71df2ab94f5462185b

Patch0:         0001-Do-not-write-after-the-end-of-the-array-and-overwrit.patch
Patch1:         tmux-CVE-2022-47016.patch

Requires:       libevent ncurses

BuildRequires:  libevent-devel
BuildRequires:  ncurses-devel
BuildRequires:  bison

%description
Terminal multiplexer

%prep
%autosetup -p1

%build
sh autogen.sh
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %dir %{_libdir}/debug
%{_datadir}/*
%exclude %{_usrsrc}

%changelog
* Wed Feb 01 2023 Harinadh D <hdommaraju@vmware.com> 3.1b-4
- fix CVE-2022-47016
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.1b-3
- Exclude debug symbols properly
* Wed May 12 2021 Michelle Wang <michellew@vmware.com> 3.1b-2
- Add patch for CVE-2020-27347
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
