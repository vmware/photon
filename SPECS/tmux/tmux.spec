Summary:        Terminal multiplexer
Name:           tmux
Version:        2.7
Release:        2%{?dist}
License:        GPLv3+
URL:            https://tmux.github.io
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=7839ef748ea55df8c02c727047f65bd235b5e3b8ab23157246071e1b9954fa269594da9fbd0fabf6a850e3b5dfda962a0a067c1507411c92a84d1db2666ecf37

Requires: libevent
Requires: ncurses

BuildRequires: libevent-devel
BuildRequires: ncurses-devel
BuildRequires: bison

%description
Terminal multiplexer

%prep
%autosetup -p1

%build
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
%{_datadir}/*
%exclude %{_usrsrc}
%exclude %dir %{_libdir}/debug

%changelog
* Sat Mar 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.7-2
- Exclude debug symbols properly
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.7-1
- Updated to version 2.7.
* Tue May 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4-1
- Updated to version 2.4. Added make check.
* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
- Updated to version 2.3.
* Wed Jul 13 2016 Alexey Makhalov <amakhalov@vmware.com> 2.2-1
- Initial build.  First version
