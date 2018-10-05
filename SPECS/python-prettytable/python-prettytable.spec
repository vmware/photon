%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-prettytable
Version:        0.7.2
Release:        6%{?dist}
Summary:        Library for displaying tabular data in a visually appealing ASCII format
License:        BSD-2-Clause
Group:          Development/Languages/Python
URL:            http://code.google.com/p/prettytable/
Source0:        prettytable-%{version}.tar.gz
%define sha1 prettytable=b7d0bf0feee0d23108a044ffae44aff5c5935250

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
PrettyTable is a simple Python library designed to make it quick and easy to
represent tabular data in visually appealing ASCII tables. It was inspired by
the ASCII tables used in the PostgreSQL shell psql. PrettyTable allows for
selection of which columns are to be printed, independent alignment of columns
(left or right justified or centred) and printing of "sub-tables" by
specifying a row range.


%package -n     python3-prettytable
Summary:        python-prettytable

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-prettytable
Python 3 version.

%prep
%setup -n prettytable-%{version}
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
python2 prettytable_test.py
pushd ../p3dir
LANG=en_US.UTF-8 python3 prettytable_test.py
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-prettytable
%defattr(-,root,root,-)
%{python3_sitelib}/*


%changelog
*   Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 0.7.2-6
-   Fixed rpm check errors
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.2-5
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> 0.7.2-4
-   Adding python3 support.
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 0.7.2-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.2-2
-   GA - Bump release of all rpms
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
