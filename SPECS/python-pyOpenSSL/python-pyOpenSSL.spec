%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Python wrapper module around the OpenSSL library
Name:           python-pyOpenSSL
Version:        16.2.0
Release:        3%{?dist}
Url:            https://github.com/pyca/pyopenssl
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pyopenssl-%{version}.tar.gz
%define sha1    pyopenssl=fdcaa88c9cf814b35cb9e1f6065adca6110cedcc
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs
Requires:       python-cryptography
Requires:       python-enum
Requires:       python-ipaddress

BuildArch:      noarch

%description
High-level wrapper around a subset of the OpenSSL library.

%package -n     python3-pyOpenSSL
Summary:        Python 3 version
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       python3-cryptography

%description -n python3-pyOpenSSL
Python 3 version.

%prep
%setup -q -n pyopenssl-%{version}

%build
python setup.py build
python3 setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python setup.py test
python3 setup.py test

%files
%defattr(-,root,root)
%{python_sitelib}/*

%files -n python3-pyOpenSSL
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Tue Feb 21 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-2
-   Add Requires for python-enum and python-ipaddress
*   Tue Feb 14 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-1
-   Initial packaging for Photon
