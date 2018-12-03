%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-ConcurrentLogHandler
Version:        0.9.1
Release:        3%{?dist}
Summary:        Concurrent logging handler (drop-in replacement for RotatingFileHandler) Python 2.6+
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/ConcurrentLogHandler/0.9.1
Source0:        ConcurrentLogHandler-%{version}.tar.gz
%define sha1    ConcurrentLogHandler=9afcd87b6eb0f37f65b8d7eb928c6d20415692ab
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools

BuildArch:      noarch

%description
ConcurrentLogHandler is a module that provides an additional log handler for Python’s standard logging package (PEP 282). This handler will write log events to log file which is rotated when the log file reaches a certain size. Multiple processes can safely write to the same log file concurrently.

%package -n     python3-ConcurrentLogHandler
Summary:        python-ConcurrentLogHandler
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools

%description -n python3-ConcurrentLogHandler
Python 3 version.

%prep
%setup -n ConcurrentLogHandler-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python_sitelib} \
python2 stresstest.py
pushd ../p3dir
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 stresstest.py
popd

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%doc /usr/docs/LICENSE
%doc /usr/docs/README
%exclude /usr/tests/stresstest.py

%files -n python3-ConcurrentLogHandler
%defattr(-,root,root,-)
%{python3_sitelib}/*
%exclude /usr/tests/stresstest.py

%changelog
*   Mon Dec 03 2018 Ashwin H <ashwinh@vmware.com> 0.9.1-3
-   Add %check
*   Thu Sep 21 2017 Bo Gan <ganb@vmware.com> 0.9.1-2
-   Disable test as no tests are available
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.9.1-1
-   Initial version of python-ConcurrentLogHandler package for Photon.
