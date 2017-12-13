%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-singledispatch
Version:        3.4.0.3
Release:        1%{?dist}
Summary:        This library brings functools.singledispatch from Python 3.4 to Python 2.6-3.3
License:        PSFL
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/singledispatch
Source0:        https://pypi.python.org/packages/d9/e9/513ad8dc17210db12cb14f2d4d190d618fb87dd38814203ea71c87ba5b68/singledispatch-3.4.0.3.tar.gz
%define sha1 singledispatch=f93241b06754a612af8bb7aa208c4d1805637022

Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description


%prep
%setup -n singledispatch-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Mon Dec 11 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 3.4.0.3-1
-   Initial version of python singledispatch for PhotonOS.
