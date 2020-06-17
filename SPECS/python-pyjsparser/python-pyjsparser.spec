%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Fast javascript parser (based on esprima.js).
Name:           python3-pyjsparser
Version:        2.7.1
Release:        2%{?dist}
License:        MIT License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/pyjsparser/2.5.2
Source0:        https://files.pythonhosted.org/packages/source/p/pyjsparser/pyjsparser-%{version}.tar.gz
%define         sha1 pyjsparser=760fc7a1dacefa484fea4b0c4273973eb6af76b2
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Fast javascript parser (based on esprima.js).


%prep
%setup -q -n pyjsparser-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

#%check
#This package does not come with a test suite.

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 2.7.1-2
-   Mass removal python2
*   Sun Nov 10 2019 Tapas Kundu <tkundu@vmware.com> 2.7.1-1
-   Update to 2.7.1
*   Mon Sep 11 2017 Xiaolin Li <xiaolinl@vmware.com> 2.5.2-1
-   Initial packaging for Photon
