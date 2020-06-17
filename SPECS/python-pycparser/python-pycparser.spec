%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python C parser
Name:           python3-pycparser
Version:        2.18
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/pycparser
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/p/pycparser/pycparser-%{version}.tar.gz
%define sha1    pycparser=1c75af69ae6273b1f1f531744f87d060965ed85d

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs
BuildArch:      noarch


%description
pycparser is a complete parser of the C language, written in pure Python using the PLY parsing library. It parses C code into an AST and can serve as a front-end for C compilers or analysis tools.


%prep
%setup -q -n pycparser-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
cd tests
python3 all_tests.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 2.18-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.18-1
-   Update to version 2.18
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.17-3
-   Use python2 instead of python
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.17-2
-   Fix arch
*   Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.17-1
-   Updated to version 2.17.
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.14-4
-   Added python3 site-packages.
*   Tue Oct 04 2016 ChangLee <changlee@vmware.com> 2.14-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.14-2
-   GA - Bump release of all rpms
*   Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.14-1
-   Initial packaging for Photon
