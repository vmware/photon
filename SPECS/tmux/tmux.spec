Summary:        Terminal multiplexer
Name:           tmux
Version:        3.1b
Release:        1%{?dist}
License:        GPLv3+
URL:            https://tmux.github.io/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha1    tmux=727ae2ecdf0e420aa5b5a210d61ef2794bbc03d8
Requires:       libevent ncurses
BuildRequires:  libevent-devel ncurses-devel

%description
Terminal multiplexer

%prep
%setup -q

%build
sh autogen.sh
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make  %{?_smp_mflags} check

%files
%defattr(-,root,root)
/usr/bin/*
%exclude /usr/lib
/usr/share/*
%exclude /usr/src

%changelog
*   Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1b-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.7-1
-   Updated to version 2.7.
*   Tue May 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4-1
-   Updated to version 2.4. Added make check.
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
-   Updated to version 2.3.
*   Wed Jul 13 2016 Alexey Makhalov <amakhalov@vmware.com> 2.2-1
-   Initial build.  First version
