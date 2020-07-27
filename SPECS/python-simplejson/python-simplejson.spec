%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Simple, fast, extensible JSON encoder/decoder for Python.
Name:           python3-simplejson
Version:        3.17.2
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/simplejson
Source0:        simplejson-%{version}.tar.gz
%define sha1    simplejson=ed38d765ad1b58862905aa25d13c95b134f03f5a

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel

Requires:       python3
Requires:       python3-libs

%description
simplejson is a simple, fast, complete, correct and extensible JSON <http://json.org> encoder and decoder for Python 2.5+ and Python 3.3+. It is pure Python code with no dependencies, but includes an optional C extension for a serious speed boost.


%prep
%setup -q -n simplejson-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.17.2-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 3.16.1-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.16.1-1
-   Update to version 3.16.1
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.10.0-2
-   Use python2 explicitly
*   Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.0-1
-   Initial packaging for Photon
