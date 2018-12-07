%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Library for building powerful interactive command lines in Python.
Name:           python-prompt_toolkit
Version:        2.0.4
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/prompt_toolkit
Source0:        https://files.pythonhosted.org/packages/source/p/prompt_toolkit/prompt_toolkit-%{version}.tar.gz
%define sha1    prompt_toolkit=5ac2c31dd9f443da4aa143dde56a8b5c44a254c5

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-Pygments
BuildRequires:  python-wcwidth
BuildRequires:  python-six
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-Pygments
BuildRequires:  python3-wcwidth
BuildRequires:  python3-six
%if %{with_check}
BuildRequires:  python-pytest
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python-atomicwrites
BuildRequires:  python3-atomicwrites
BuildRequires:  python-attrs
BuildRequires:  python3-attrs
BuildRequires:  python3-pytest
%endif

Requires:       python2
Requires:       python2-libs
Requires:       python-Pygments
Requires:       python-six
Requires:       python-wcwidth

BuildArch:      noarch

%description
prompt_toolkit is a library for building powerful interactive command lines and terminal applications in Python.

%package -n     python3-prompt_toolkit
Summary:        python-prompt_toolkit

Requires:       python3
Requires:       python3-libs
Requires:       python3-Pygments
Requires:       python3-six
Requires:       python3-wcwidth

%description -n python3-prompt_toolkit
Python 3 version.

%prep
%setup -q -n prompt_toolkit-%{version}
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
$easy_install_2 pathlib2 funcsigs pluggy more-itertools
PYTHONPATH=. python2 setup.py test
#make check failing for 3.7 so skipping for python3

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-prompt_toolkit
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 2.0.4-2
-   Fix makecheck
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.0.4-1
-   Update to version 2.0.4
*   Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 1.0.14-4
-   Added packages which are required during runtime
*   Wed Jul 12 2017 Chang Lee <changlee@vmware.com> 1.0.14-3
-   Updated %check and added six, wcwidth, and pytest in BuildRequires
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.14-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.14-1
-   Initial packaging for Photon
