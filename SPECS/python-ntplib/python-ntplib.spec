%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python NTP library
Name:           python-ntplib
Version:        0.3.3
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/ntplib/
Source0:        ntplib-%{version}.tar.gz
%define         sha1 ntplib=403ac0cc01398bacdf608d4aa35e74e36f5ad64d

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-incremental

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
This module offers a simple interface to query NTP servers from Python.

It also provides utility functions to translate NTP fields values to text (mode, leap indicator…). Since it’s pure Python, and only depends on core modules, it should work on any platform with a Python implementation.

%package -n     python3-ntplib
Summary:        python-ntplib
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs
%description -n python3-ntplib
Python 3 version.

%prep
%setup -q -n ntplib-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
python3 setup.py build

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

#%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-ntplib
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 0.3.3-2
-   Removed %check due to no test existence.
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.3.3-1
-   Initial packaging for Photon.