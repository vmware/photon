Summary:         Multithreaded IO generation tool
Name:            fio
Version:         3.30
Release:         1%{?dist}
License:         GPLv2
Group:           Applications/System
Vendor:          VMware, Inc.
Distribution:    Photon
URL:             http://git.kernel.dk/?p=fio.git;a=summary
Source0:         https://git.kernel.org/pub/scm/linux/kernel/git/axboe/fio.git/snapshot/%{name}-%{version}.tar.gz
%define sha512   %{name}=ab4feb956ed650b238240f43e7bd3ac63c50e668b6e056c5ac2869c192796396b4c46b7e4b98ed74dd3ca5cc0aa5cb1c09f5c0e05bd2980441377ce2658f16ab
BuildRequires:   gcc
BuildRequires:   gnupg
BuildRequires:   zlib-devel
BuildRequires:   python3-devel
BuildRequires:   curl-devel
BuildRequires:   openssl-devel
BuildRequires:   make

%description
Fio spawns a number of threads or processes doing a particular type of I/O
action as specified by the user. fio takes a number of global parameters, each
inherited by the thread unless otherwise parameters given to them overriding
that setting is given. The typical use of fio is to write a job file matching
the I/O load one wants to simulate.

%package docs
Summary: Files needed for development using %{name} protocol
Requires: %{name} = %{version}-%{release}

%description docs
Package %{name}-docs provide man pages and other docs related to fio.

%prep
%autosetup -p1

%build
sh ./configure
%make_build

%install
%make_install prefix=%{_prefix} mandir=%{_mandir}

%files
%defattr(-,root,root)
%doc MORAL-LICENSE GFIO-TODO SERVER-TODO STEADYSTATE-TODO
%license COPYING
%dir %{_datadir}/%{name}
%{_bindir}/*
%{_datadir}/%{name}/*

%files docs
%defattr(-,root,root)
%doc README.rst REPORTING-BUGS HOWTO.rst examples
%{_mandir}/man1/*

%changelog
* Mon Jun 06 2022 Piyush Gupta <gpiyush@vmware.com> 3.30-1
- Initial packaging for Photon OS.
