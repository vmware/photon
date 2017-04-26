Summary:       Python documentation generator
Name:          python-sphinx
Version:       1.5.3
Release:       1%{?dist}
Group:         Development/Tools
Vendor:        VMware, Inc.
License:       BSD-2-Clause
URL:           http://www.vmware.com
Source0:       https://pypi.python.org/packages/a7/df/4487783152b14f2b7cd0b0c9afb119b262c584bf972b90ab544b61b74c62/Sphinx-%{version}.tar.gz
%define sha1 Sphinx=e296be1f697ba5eda7941570d718544df8182648
Distribution:  Photon
BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: python-setuptools

Requires:       python2

BuildArch:      noarch

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
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.5.3-1
-   Upgrade version to 1.5.3
*   Fri Dec 16 2016 Dheeraj Shetty <dheerajs@vmware.com> 1.5.1-1
-   Initial
