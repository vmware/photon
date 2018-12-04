%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

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

%package -n     python3-tornado
Summary:        python3 version 
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n python3-tornado
Python 3 version.



%prep
%setup -n tornado-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-tornado
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Dec 04 2018 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-1
-   To build python2 and python3 tornado packages
*   Mon Dec 11 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-1
-   Initial version of python tornado for PhotonOS.

