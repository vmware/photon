%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-py
Version:        1.6.0
Release:        2%{?dist}
Summary:        Python development support library
License:        MIT
Group:          Development/Languages/Python
Url:            https://github.com/pytest-dev/py
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/53/72/6c6f1e787d9cab2cc733cf042f125abec07209a58308831c9f292504e826/py-%{version}.tar.gz
%define sha1    py=b7196e40ff311d5f44e3bed2e0d3477f4f19559b

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
The py lib is a Python development support library featuring the following tools and modules:

py.path: uniform local and svn path objects
py.apipkg: explicit API control and lazy-importing
py.iniconfig: easy parsing of .ini files
py.code: dynamic code generation and introspection


%prep
%setup -n py-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
#python-py and python-pytest have circular dependency. Hence not adding tests
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 1.6.0-2
-   Mass removal python2
*   Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 1.6.0-1
-   Updated to versiob 1.6.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.4.33-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.33-2
-   Use python2_sitelib
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.33-1
-   Initial
