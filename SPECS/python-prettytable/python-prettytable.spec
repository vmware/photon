Name:           python-prettytable
Version:        0.7.2
Release:        2%{?dist}
Summary:        Library for displaying tabular data in a visually appealing ASCII format
License:        BSD-2-Clause
Group:          Development/Languages/Python
Url:            http://code.google.com/p/prettytable/
Source0:        prettytable-%{version}.tar.gz
%define sha1 prettytable=b7d0bf0feee0d23108a044ffae44aff5c5935250

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires: python2
Requires: python2-libs

BuildArch:      noarch

%description
PrettyTable is a simple Python library designed to make it quick and easy to
represent tabular data in visually appealing ASCII tables. It was inspired by
the ASCII tables used in the PostgreSQL shell psql. PrettyTable allows for
selection of which columns are to be printed, independent alignment of columns
(left or right justified or centred) and printing of "sub-tables" by
specifying a row range.

%prep
%setup -n prettytable-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python prettytable_test.py

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.2-2
-	GA - Bump release of all rpms
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
