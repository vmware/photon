%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Core utilities for Python packages
Name:           python-packaging
Version:        16.8
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/packaging
License:        BSD or ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pypi.python.org/packages/source/p/packaging/packaging-%{version}.tar.gz
%define sha1    packaging=68f9574b50683c0962ad90346879e7a2319cc6d8
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%package -n     python3-packaging
Summary:        python-packaging
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-packaging

Python 3 version.

%prep
%setup -q -n packaging-%{version}
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
python3 setup.py test

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-packaging
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 16.8-2
-   Remove python-setuptools from BuildRequires
*   Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> 16.8-1
-   Initial packaging for Photon
