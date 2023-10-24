Name:           scons
Version:        4.5.2
Release:        1%{?dist}
Summary:        An Open Source software construction tool
Group:          Development/Tools
License:        MIT
URL:            https://sourceforge.net/projects/scons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://sourceforge.net/projects/scons/files/scons/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=a9675f4b4dbedf8c7375d4d099216cd935c38944d57b0a08de2b9c133bb53184de0d5803edf5cb9f800f205b1252ceca3aaf33a10bf5d8b48eacd58866cf776c

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3-xml
Requires:       python3

BuildArch:      noarch

%description
SCons is an Open Source software construction tool—that is, a next-generation build tool.
Think of SCons as an improved, cross-platform substitute for the classic Make utility
with integrated functionality similar to autoconf/automake and compiler caches such as ccache.
In short, SCons is an easier, more reliable and faster way to build software.

%prep
%autosetup -p1 -n SCons-%{version}

%build
%{py3_build}

%install
%py3_install -- --install-data=%{_datadir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/*
%{_datadir}/*.1

%changelog
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.5.2-1
- Ugrade to v4.5.2
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 4.1.0-2
- Update release to compile with python 3.11
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 4.1.0-1
- Automatic Version Bump
* Fri Sep 18 2020 Susant Sahani <ssahani@vmware.com> 4.0.1-2
- Add requires python3-xml
* Wed Jul 29 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.1-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 3.0.1-3
- Build with python3
- Mass removal python2
* Mon Jan 07 2019 Alexey Makhalov <amakhalov@vmware.com> 3.0.1-2
- BuildRequires: python2
* Tue Sep 18 2018 Srinidhi Rao <srinidhir@vmware.com> 3.0.1-1
- Upgraded to version 3.0.1
* Sun Oct 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.1-1
- Initial build. First version
