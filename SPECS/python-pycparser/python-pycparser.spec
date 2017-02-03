%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Python C parser
Name:           python-pycparser
Version:        2.14
Release:        4%{?dist}
Url:            https://pypi.python.org/pypi/pycparser
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/p/pycparser/pycparser-2.14.tar.gz
%define sha1    pycparser=922162bad4aa8503988035506c1c65bbf8690ba4

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs


%description
pycparser is a complete parser of the C language, written in pure Python using the PLY parsing library. It parses C code into an AST and can serve as a front-end for C compilers or analysis tools. 

%package -n     python3-pycparser
Summary:        python-pycparser
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n python3-pycparser
Python 3 version.

%prep
%setup -q -n pycparser-%{version}

%build
python setup.py build
python3 setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
cd tests
python all_tests.py

%files
%defattr(-,root,root)
%{python_sitelib}/*

%files -n python3-pycparser
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.14-4
-   Added python3 site-packages.
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 2.14-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.14-2
-   GA - Bump release of all rpms
*   Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.14-1
-   Initial packaging for Photon
