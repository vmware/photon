%define debug_package %{nil}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        dis3 is a Python 2.7 backport of the dis module from Python 3.5.
Name:           python-dis3
Version:        0.1.3
Release:        1%{?dist}
Url:            https://pypi.org/project/dis3
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/b1/b8/2a5845f47cd3cc5fc149d9d4a06dd5a8163bcaf91fb82ed26903ce8a3def/dis3-%{version}.tar.gz
%define sha1    dis3=58e4654f522845b1f5616a2d1b5112063e0f625f
BuildRequires:  python2
BuildRequires:  python-xml
BuildRequires:  python-setuptools

Requires:       python2

%description
dis3 is a Python 2.7 backport of the dis module from Python 3.5.

%prep
%setup -q -n dis3-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --skip-build --root=%{buildroot}

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%changelog
*   Thu Feb 11 2021 Ankit Jain <ankitja@vmware.com> 0.1.3-1
-   Initial packaging
