%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Fast javascript parser (based on esprima.js).
Name:           python-pyjsparser
Version:        2.5.2
Release:        1%{?dist}
License:        MIT License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/pyjsparser/2.5.2
Source0:        https://files.pythonhosted.org/packages/source/p/pyjsparser/pyjsparser-%{version}.tar.gz
%define         sha1 pyjsparser=5a03ca6042b2f5bb2226158c8e7f15210f4eb38e
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Fast javascript parser (based on esprima.js).

%package -n     python3-pyjsparser
Summary:        python-pyjsparser
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-six
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs

%description -n python3-pyjsparser
Python 3 version.

%prep
%setup -q -n pyjsparser-%{version}
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

#%check
#This package does not come with a test suite.

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-pyjsparser
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon Sep 11 2017 Xiaolin Li <xiaolinl@vmware.com> 2.5.2-1
-   Initial packaging for Photon
