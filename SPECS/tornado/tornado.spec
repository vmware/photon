%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           tornado
Version:        4.5.2
Release:        1%{?dist}
Summary:        Tornado is a Python web framework and asynchronous networking library
License:        PSFL
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/tornado
Source0:        https://pypi.python.org/packages/fa/14/52e2072197dd0e63589e875ebf5984c91a027121262aa08f71a49b958359/tornado-4.5.2.tar.gz
%define sha1 tornado=27a7690aae925c6ec6450830befccc11fe3dfecf

Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      x86_64

%description


%prep
%setup -n tornado-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Mon Dec 11 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-1
-   Initial version of python tornado for PhotonOS.
