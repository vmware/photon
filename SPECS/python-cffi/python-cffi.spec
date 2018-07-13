%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Interface for Python to call C code
Name:           python-cffi
Version:        1.9.1
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/cffi
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/c/cffi/cffi-%{version}.tar.gz
%define sha1    cffi=16265a4b305d433fb9089b19278502e904b0cb43

Patch0:	python-cffi-fix-mem-leak.patch
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  libffi
BuildRequires:  python-pycparser
Requires:       python2
Requires:       python2-libs
Requires:       python-pycparser

%description
Foreign Function Interface for Python, providing a convenient and reliable way of calling existing C code from Python. The interface is based on LuaJIT’s FFI.


%package -n     python3-cffi
Summary:        python-cffi
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pycparser
Requires:       python3-pycparser
Requires:       python3
Requires:       python3-libs

%description -n python3-cffi
Python 3 version.


%prep
%setup -q -n cffi-%{version}
%patch0 -p1

%build
python setup.py build
python3 setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%files -n python3-cffi
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jul 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.9.1-3
-   Fix memory leak in python-cffi libobj module
*   Mon Dec 04 2017 Kumar Kaushik <kaushikk@vmware.com> 1.9.1-2
-   Release bump to use python 3.5.4.
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.1-1
-   Updated to version 1.9.1.
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.2-3
-   Added python3 site-packages.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.2-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.2-1
-   Updated to version 1.5.2
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.5.0-1
-   Upgrade version
*   Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.3.0-1
-   nitial packaging for Photon
