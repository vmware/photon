%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python PAM module using ctypes, py3/py2
Name:           python-pam
Version:        1.8.2
Release:        2%{?dist}
URL:            https://pypi.python.org/pypi/python-pam/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        python-pam-%{version}.tar.gz
%define sha1    python-pam=a28881d2c0a86297a0d45d2558c7381621480a76

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python2
Requires:       python2-libs

%description
Python PAM module using ctypes, py3/py2.

%package -n     python3-pam
Summary:        python-pam

Requires:       python3
Requires:       python3-libs

%description -n python3-pam

Python 3 version.

%prep
%setup -q -n python-pam-%{version}
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

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-pam
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.2-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Mar 09 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.2-1
-   Initial packaging for Photon
