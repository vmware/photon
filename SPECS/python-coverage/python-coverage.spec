%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python2_version: %define python2_version %(python2 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        Code coverage measurement for Python.
Name:           python-coverage
Version:        4.3.4
Release:        5%{?dist}
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/coverage
Source0:        https://files.pythonhosted.org/packages/source/c/coverage/coverage-%{version}.tar.gz
%define         sha1 coverage=8ffe985cb6efd4b747fd8ee75a9a41e4f319cc71

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  python-pytest
BuildRequires:  python-six
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-xml

%description
Code coverage measurement for Python.
Coverage.py measures code coverage, typically during test execution. It uses the code analysis tools and tracing hooks provided in the Python standard library to determine which lines are executable, and which have been executed.

%package -n     python3-coverage
Summary:        python-coverage
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-six
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-xml

%description -n python3-coverage
Python 3 version.

%prep
%setup -q -n coverage-%{version}
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
easy_install tox
easy_install PyContracts
LANG=en_US.UTF-8 tox -e py27
pushd ../p3dir
LANG=en_US.UTF-8 tox -e py36
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/coverage2
%{_bindir}/coverage-%{python2_version}

%files -n python3-coverage
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/coverage
%{_bindir}/coverage3
%{_bindir}/coverage-%{python3_version}

%changelog
*   Thu Aug 10 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.4-5
-   Fixed make check errors
*   Fri Jul 07 2017 Chang Lee <changlee@vmware.com> 4.3.4-4
-   Add python-xml and pyhton3-xml to  Requires.
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.4-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.3.4-2
-   Packaging python2 and oython3 scripts in bin directory
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.4-1
-   Initial packaging for Photon
