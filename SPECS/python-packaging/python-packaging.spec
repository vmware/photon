%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Core utilities for Python packages
Name:           python-packaging
Version:        17.1
Release:        1%{?dist}
URL:            https://pypi.python.org/pypi/packaging
License:        BSD or ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        pypi.python.org/packages/source/p/packaging/packaging-%{version}.tar.gz
%define sha1    packaging=8dbd54a645fcc7951fcd6c06e9ac6494a0ada816
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%if %{with_check}
BuildRequires:  python-pytest
BuildRequires:  python-pyparsing
BuildRequires:  python-six
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pytest
BuildRequires:  python3-pyparsing
BuildRequires:  python3-six
%endif

Requires:       python2
Requires:       python2-libs
Requires:       python-pyparsing
Requires:       python-six

BuildArch:      noarch

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%package -n     python3-packaging
Summary:        python-packaging

Requires:       python3
Requires:       python3-libs
Requires:       python3-pyparsing
Requires:       python3-six

%description -n python3-packaging

Python 3 version.

%prep
%setup -q -n packaging-%{version}
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
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 pretend
PYTHONPATH=./ py.test2

easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pretend
PYTHONPATH=./ py.test3

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-packaging
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.1-1
-   Update to version 17.1
*   Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 16.8-4
-   Fixed rpm check errors
-   Fixed runtime dependencies
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 16.8-3
-   Fix arch
*   Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 16.8-2
-   Remove python-setuptools from BuildRequires
*   Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> 16.8-1
-   Initial packaging for Photon
