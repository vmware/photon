%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           scons
Version:        3.0.1
Release:        1%{?dist}
Summary:        An Open Source software construction tool
Group:          Development/Tools
License:        MIT
URL:            http://scons.org
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha1    scons=498691cf8d4f6da971b99fab0c3480ef944c4d1e
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       python2
BuildArch:      noarch

%description
SCons is an Open Source software construction tool—that is, a next-generation build tool.
Think of SCons as an improved, cross-platform substitute for the classic Make utility
with integrated functionality similar to autoconf/automake and compiler caches such as ccache.
In short, SCons is an easier, more reliable and faster way to build software.

%prep
%setup -q

%build
python setup.py build

%install
python setup.py install \
    --root=%{buildroot} \
    --prefix=%{_prefix} \
    --standard-lib \
    --optimize=1 \
    --install-data=%{_datadir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
%{_bindir}/*
%{_datadir}/*

%changelog
*   Tue Sep 18 2018 Srinidhi Rao <srinidhir@vmware.com> 3.0.1-1
-   Upgraded to version 3.0.1
*   Sun Oct 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.1-1
-   Initial build.  First version
