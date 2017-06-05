%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Simple, fast, extensible JSON encoder/decoder for Python.
Name:           python-simplejson
Version:        3.10.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/simplejson
Source0:        simplejson-%{version}.tar.gz
%define sha1    simplejson=dffc85c6851430578acf138c2a1193bc89a3eb0f

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
simplejson is a simple, fast, complete, correct and extensible JSON <http://json.org> encoder and decoder for Python 2.5+ and Python 3.3+. It is pure Python code with no dependencies, but includes an optional C extension for a serious speed boost.

%package -n     python3-simplejson
Summary:        python-simplejson
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n python3-simplejson
Python 3 version.

%prep
%setup -q -n simplejson-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-simplejson
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.10.0-2
-   Use python2 explicitly
*   Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.0-1
-   Initial packaging for Photon
