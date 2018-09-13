%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-py
Version:        1.6.0
Release:        1%{?dist}
Summary:        Python development support library
License:        MIT
Group:          Development/Languages/Python
Url:            https://github.com/pytest-dev/py
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/53/72/6c6f1e787d9cab2cc733cf042f125abec07209a58308831c9f292504e826/py-%{version}.tar.gz
%define sha1    py=b7196e40ff311d5f44e3bed2e0d3477f4f19559b

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-setuptools_scm
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
The py lib is a Python development support library featuring the following tools and modules:

py.path: uniform local and svn path objects
py.apipkg: explicit API control and lazy-importing
py.iniconfig: easy parsing of .ini files
py.code: dynamic code generation and introspection

%package -n     python3-py
Summary:        Python development support library
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-py

Python 3 version.

%prep
%setup -n py-%{version}
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
#python-py and python-pytest have circular dependency. Hence not adding tests
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-py
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 1.6.0-1
-   Updated to versiob 1.6.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.4.33-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.33-2
-   Use python2_sitelib
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.33-1
-   Initial
