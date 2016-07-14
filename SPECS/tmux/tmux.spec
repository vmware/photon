Summary:	Terminal multiplexer
Name:		tmux
Version:	2.2
Release:	1%{?dist}
License:	GPLv3+
URL:		https://tmux.github.io/
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha1 tmux=5ed1430bc7ef44c227e64e9401c686573dd0791a
Requires:	libevent ncurses
BuildRequires:	libevent-devel ncurses-devel
%description
Terminal multiplexer
%prep
%setup -q
%build
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
*	Wed Jul 13 2016 Alexey Makhalov <amakhalov@vmware.com> 2.2-1
-	Initial build.	First version
