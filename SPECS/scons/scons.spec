%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           scons
Version:        4.0.1
Release:        2%{?dist}
Summary:        An Open Source software construction tool
Group:          Development/Tools
License:        MIT
URL:            http://scons.org
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha1    scons=dac73a0fb65e2cc3714ba0ee679e7b4b1e645e28
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
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
%setup -q

%build
python3 setup.py build

%install
python3 setup.py install \
    --root=%{buildroot} \
    --prefix=%{_prefix} \
    --optimize=1 \
    --install-data=%{_datadir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
*   Fri Sep 18 2020 Susant Sahani <ssahani@vmware.com> 4.0.1-2
-   Add requires python3-xml
*   Wed Jul 29 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.1-1
-   Automatic Version Bump
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 3.0.1-3
-   Build with python3
-   Mass removal python2
*   Mon Jan 07 2019 Alexey Makhalov <amakhalov@vmware.com> 3.0.1-2
-   BuildRequires: python2
*   Tue Sep 18 2018 Srinidhi Rao <srinidhir@vmware.com> 3.0.1-1
-   Upgraded to version 3.0.1
*   Sun Oct 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.1-1
-   Initial build. First version
