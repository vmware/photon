Summary:        Terminal multiplexer
Name:           tmux
Version:        3.1b
Release:        3%{?dist}
License:        GPLv3+
URL:            https://tmux.github.io
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha1 %{name}=727ae2ecdf0e420aa5b5a210d61ef2794bbc03d8

Patch0:         0001-Do-not-write-after-the-end-of-the-array-and-overwrit.patch

Requires:       libevent ncurses

BuildRequires:  libevent-devel ncurses-devel

%description
Terminal multiplexer

%prep
%autosetup -p1

%build
sh autogen.sh
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

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
