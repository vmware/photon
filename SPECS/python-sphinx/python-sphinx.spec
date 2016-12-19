Summary:       Python documentation generator
Name:          python-sphinx
Version:       1.5.1
Release:       1%{?dist}
Group:         Development/Tools
Vendor:        VMware, Inc.
License:       BSD-2-Clause
URL:           http://www.vmware.com
Source0:       https://files.pythonhosted.org/packages/source/S/Sphinx/Sphinx-%{version}.tar.gz
%define sha1 Sphinx=4c413bd6310f4452c5fbeb9493065fc3dd968210
Distribution:  Photon
BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: python-setuptools

Requires:       python2

%description
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

%prep
%setup -q -n Sphinx-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{python_sitelib}/*

%changelog
*   Fri Dec 16 2016 Dheeraj Shetty <dheerajs@vmware.com> 1.5.1-1
-   Initial
