Summary:	File manager
Name:		mc
Version:	4.8.25
Release:	2%{?dist}
License:	GPLv3+
URL:		https://www.midnight-commander.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon

Source0:	http://ftp.midnight-commander.orgtar/%{name}-%{version}.tar.xz
%define sha1 mc=4082ae830f09e919112aa3fc1d7e5333921a6a33

Patch0:		disable-extfs-test.patch

Requires:	glib
Requires:	pcre
Requires:	slang

BuildRequires:	glib-devel
BuildRequires:	pcre-devel
BuildRequires:	slang-devel

%description
MC (Midnight Commander) is a text-mode full-screen file manager and visual shell

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%if 0%{?with_check}
make %{?_smp_mflags} -k check
%endif

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%exclude %dir %{_libdir}
%{_libexecdir}/*
%{_datadir}/*
%exclude %dir %{_usrsrc}

%changelog
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.8.25-2
- Exclude debug symbols properly
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
