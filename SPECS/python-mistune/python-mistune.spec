%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The fastest markdown parser in pure Python.
Name:           python-mistune
Version:        0.7.4
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/mistune/
Source0:        https://files.pythonhosted.org/packages/source/m/mistune/mistune-%{version}.tar.gz
%define         sha1 mistune=23adb8fe73662bfc0f1b21009a8df2fc9affd4aa

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
The fastest markdown parser in pure Python

The fastest markdown parser in pure Python with renderer features, inspired by marked.

%package -n     python3-mistune
Summary:        python-mistune
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-mistune
Python 3 version.

%prep
%setup -q -n mistune-%{version}
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

%files -n python3-mistune
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-1
-   Initial packaging for Photon
