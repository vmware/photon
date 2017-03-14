%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python parsing module.
Name:           python-pyparsing
Version:        2.1.10
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/pyparsing/2.1.10
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pyparsing-%{version}.tar.gz
%define sha1    pyparsing=3fc0a5109b6b178899927b773f77a32d504ee00f

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
Python parsing module.

%package -n     python3-pyparsing
Summary:        python-pyparsing
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-pyparsing

Python 3 version.

%prep
%setup -q -n pyparsing-%{version}
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

%files -n python3-pyparsing
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.10-1
-   Initial packaging for Photon
