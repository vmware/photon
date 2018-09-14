%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pure Python JavaScript Translator/Interpreter.
Name:           python-Js2Py
Version:        0.59
Release:        1%{?dist}
License:        MIT License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Js2Py
Source0:        https://files.pythonhosted.org/packages/source/J/Js2Py/Js2Py-%{version}.tar.gz
%define         sha1 Js2Py=828ee742021299ee7cecccb52502288b7a4fc5fe
Patch0:         js2py-python3-print.patch
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-setuptools_scm
BuildRequires:  python-six
BuildRequires:  python-py
%if %{with_check}
BuildRequires:  python-pyjsparser
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-tzlocal
Requires:       python-pyjsparser
Requires:       python-six

BuildArch:      noarch

%description
Pure Python JavaScript Translator/Interpreter.
Everything is done in 100% pure Python so it's extremely easy to install and use. Supports Python 2 & 3. Full support for ECMAScript 5.1, ECMA 6 support is still experimental.

%package -n     python3-Js2Py
Summary:        python-Js2Py
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-six

Requires:       python3
Requires:       python3-libs
Requires:       python3-six
Requires:       python3-tzlocal
Requires:       python3-pyjsparser
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-py
%if %{with_check}
BuildRequires:  python3-pyjsparser
%endif

%description -n python3-Js2Py
Python 3 version.

%prep
%setup -q -n Js2Py-%{version}
%patch0 -p1
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

%files -n python3-Js2Py
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 0.59-1
-   Updated to version 0.59
*   Fri Sep 08 2017 Xiaolin Li <xiaolinl@vmware.com> 0.50-1
-   Initial packaging for Photon
