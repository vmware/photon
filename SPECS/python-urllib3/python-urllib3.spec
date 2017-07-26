%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A powerful, sanity-friendly HTTP client for Python.
Name:           python-urllib3
Version:        1.20
Release:        4%{?dist}
Url:            https://pypi.python.org/pypi/urllib3
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/shazow/urllib3/archive/urllib3-1.20.tar.gz
%define sha1    urllib3=2608f2069d3bb1be36da9483c24aa2a0ada38501

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:	python-pytest
BuildRequires:	python-psutil
%endif

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
urllib3 is a powerful, sanity-friendly HTTP client for Python. Much of the Python ecosystem already uses urllib3 and you should too.

%package -n     python3-urllib3
Summary:        python-urllib3
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:	python3-pytest
BuildRequires:	python3-psutil
%endif
Requires:       python3
Requires:       python3-libs

%description -n python3-urllib3
Python 3 version.

%prep
%setup -q -n urllib3-%{version}
# Dummyserver tests are failing when running in chroot. So disabling the tests.
rm -rf test/with_dummyserver/

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 mock
$easy_install_2 PySocks
$easy_install_2 nose
$easy_install_2 tornado
PYTHONPATH=./ py.test2

easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 mock
$easy_install_3 PySocks
$easy_install_3 nose
$easy_install_3 tornado
PYTHONPATH=./ py.test3

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-urllib3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-4
-   Fixed rpm check errors
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.20-2
-   Use python2 explicitly
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-1
-   Initial packaging for Photon
