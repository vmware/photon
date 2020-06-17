%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pure Python JavaScript Translator/Interpreter.
Name:           python3-Js2Py
Version:        0.66
Release:        2%{?dist}
License:        MIT License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Js2Py
Source0:        https://files.pythonhosted.org/packages/source/J/Js2Py/Js2Py-%{version}.tar.gz
%define         sha1 Js2Py=f6e8d0fc625d28ae196be1db10f800ec56ea68dd
Patch0:         js2py-python3-print.patch
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-six
BuildRequires:  python3-py
%if %{with_check}
BuildRequires:  python3-pyjsparser
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-six
Requires:       python3-tzlocal
Requires:       python3-pyjsparser

BuildArch:      noarch

%description
Pure Python JavaScript Translator/Interpreter.
Everything is done in 100% pure Python so it's extremely easy to install and use. Supports Python 2 & 3. Full support for ECMAScript 5.1, ECMA 6 support is still experimental.

%prep
%setup -q -n Js2Py-%{version}
%patch0 -p1

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

#%check
#This package does not come with a test suite.

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 0.66-2
-   Mass removal python2
*   Sun Nov 10 2019 Tapas Kundu <tkundu@vmware.com> 0.66-1
-   Updated to version 0.66
*   Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 0.59-1
-   Updated to version 0.59
*   Fri Sep 08 2017 Xiaolin Li <xiaolinl@vmware.com> 0.50-1
-   Initial packaging for Photon
