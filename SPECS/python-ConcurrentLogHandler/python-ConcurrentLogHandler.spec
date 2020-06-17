%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-ConcurrentLogHandler
Version:        0.9.1
Release:        4%{?dist}
Summary:        Concurrent logging handler (drop-in replacement for RotatingFileHandler) Python 2.6+
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/ConcurrentLogHandler/0.9.1
Source0:        ConcurrentLogHandler-%{version}.tar.gz
%define sha1    ConcurrentLogHandler=9afcd87b6eb0f37f65b8d7eb928c6d20415692ab
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools

BuildArch:      noarch

%description
ConcurrentLogHandler is a module that provides an additional log handler for Python’s standard logging package (PEP 282). This handler will write log events to log file which is rotated when the log file reaches a certain size. Multiple processes can safely write to the same log file concurrently.


%prep
%setup -n ConcurrentLogHandler-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 stresstest.py

%files
%doc /usr/docs/LICENSE
%doc /usr/docs/README
%exclude /usr/tests/stresstest.py
%{python3_sitelib}/*

%changelog
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 0.9.1-4
-   Mass removal python2
*   Mon Dec 03 2018 Ashwin H <ashwinh@vmware.com> 0.9.1-3
-   Add %check
*   Thu Sep 21 2017 Bo Gan <ganb@vmware.com> 0.9.1-2
-   Disable test as no tests are available
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.9.1-1
-   Initial version of python-ConcurrentLogHandler package for Photon.
