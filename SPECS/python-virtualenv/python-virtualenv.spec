%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-virtualenv
Version:        16.0.0
Release:        2%{?dist}
Summary:        Virtual Python Environment builder
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/virtualenv
Source0:        virtualenv-%{version}.tar.gz
%define sha1    virtualenv=33831525c360459671d25f9e5abac931c414d2f7
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-libs
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
virtualenv is a tool to create isolated Python environment.

%prep
%setup -n virtualenv-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{_bindir}/virtualenv
%{python3_sitelib}/*

%changelog
*   Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 16.0.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 16.0.0-1
-   Update to version 16.0.0
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 15.1.0-1
-   Initial version of python-virtualenv package for Photon.
