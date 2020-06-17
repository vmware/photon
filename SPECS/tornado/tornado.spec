%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-tornado
Version:        4.5.2
Release:        3%{?dist}
Summary:        Tornado is a Python web framework and asynchronous networking library
License:        PSFL
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/tornado
Source0:        https://pypi.python.org/packages/fa/14/52e2072197dd0e63589e875ebf5984c91a027121262aa08f71a49b958359/tornado-4.5.2.tar.gz
%define sha1 tornado=27a7690aae925c6ec6450830befccc11fe3dfecf

Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description


%prep
%setup -n tornado-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 4.5.2-3
-   Mass removal python2
*   Tue Dec 17 2019 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-2
-   To build python2 and python3 tornado packages
-   To remove buildArch
*   Mon Dec 11 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-1
-   Initial version of python tornado for PhotonOS.
