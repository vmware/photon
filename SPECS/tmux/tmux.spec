Summary:        Terminal multiplexer
Name:           tmux
Version:        2.3
Release:        1%{?dist}
License:        GPLv3+
URL:            https://tmux.github.io/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha1    tmux=1296585a6a4d1509f327156b5624029a62d54583
Requires:       libevent ncurses
BuildRequires:  libevent-devel ncurses-devel
%description
Terminal multiplexer
%prep
%setup -q
%build
./autogen.sh
./configure \
    --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%files
%defattr(-,root,root)
/usr/bin/*
%exclude /usr/lib
/usr/share/*
%exclude /usr/src
%changelog
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
-   Updated to version 2.3.
*   Wed Jul 13 2016 Alexey Makhalov <amakhalov@vmware.com> 2.2-1
-   Initial build.  First version
