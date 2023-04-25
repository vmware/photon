%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           scons
Version:        3.0.1
Release:        3%{?dist}
Summary:        An Open Source software construction tool
Group:          Development/Tools
License:        MIT
URL:            http://scons.org
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha512  scons=b7be40ba507366cc678f31b910553cadaf59781c3a91833a34acbd29d9cad0cda38f6753034bf92c3af55d1e0c2f72aba5d81f1ec67205d0345b005d286f7084
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3-devel
BuildRequires:  python2-devel
Requires:       python2

BuildArch:      noarch

%description
SCons is an Open Source software construction tool—that is, a next-generation build tool.
Think of SCons as an improved, cross-platform substitute for the classic Make utility
with integrated functionality similar to autoconf/automake and compiler caches such as ccache.
In short, SCons is an easier, more reliable and faster way to build software.

%prep
%autosetup

%build
%py3_build
%py3_install -- --standard-lib --prefix=%{_prefix} --optimize=1 --install-data=%{_datadir}

%py_build
%py_install -- --prefix=%{_prefix} --standard-lib --optimize=1 --install-data=%{_datadir}

# install is done in build section

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/*
%{python2_sitelib}/*
%{python3_sitelib}/*

%changelog
*   Mon May 22 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 3.0.1-3
-   Package python3 and python2 files to be compatible with both.
*   Mon Jan 06 2020 Prashant S Chauhan <psinghchauha@vmware.com> 3.0.1-2
-   Added python2 as BuildRequirement
*   Tue Sep 18 2018 Srinidhi Rao <srinidhir@vmware.com> 3.0.1-1
-   Upgraded to version 3.0.1
*   Sun Oct 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.1-1
-   Initial build.  First version
