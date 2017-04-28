%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:       Python documentation generator
Name:          python-sphinx
Version:       1.5.3
Release:       2%{?dist}
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
BuildRequires: python-babel
BuildRequires: python-docutils
BuildRequires: python-jinja2
BuildRequires: python-Pygments
BuildRequires: python-six
BuildRequires: python-alabaster
BuildRequires: python-imagesize
BuildRequires: python-requests
BuildRequires: python-snowballstemmer
BuildRequires: python-typing
BuildRequires: python-pytest
BuildRequires: python-pip

Requires:      python2
Requires:      python2-libs
Requires:      python-babel
Requires:      python-docutils
Requires:      python-jinja2
Requires:      python-Pygments
Requires:      python-six
Requires:      python-alabaster
Requires:      python-imagesize
Requires:      python-requests
Requires:      python-snowballstemmer
Requires:      python-typing

BuildArch:      noarch

%description
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

%package -n    python3-sphinx
Summary:       Python documentation generator
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-babel
BuildRequires: python3-docutils
BuildRequires: python3-jinja2
BuildRequires: python3-Pygments
BuildRequires: python3-six
BuildRequires: python3-alabaster
BuildRequires: python3-imagesize
BuildRequires: python3-requests
BuildRequires: python3-snowballstemmer
BuildRequires: python3-pytest

Requires:      python3
Requires:      python3-libs
Requires:      python3-babel
Requires:      python3-docutils
Requires:      python3-jinja2
Requires:      python3-Pygments
Requires:      python3-six
Requires:      python3-alabaster
Requires:      python3-imagesize
Requires:      python3-requests
Requires:      python3-snowballstemmer

%description -n python3-sphinx

Python 3 version.

%prep
%setup -q -n Sphinx-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%clean

%files
%defattr(-,root,root)
%{python_sitelib}/*

%files -n python3-sphinx
%defattr(-,root,root)
%{_bindir}/*
%{python3_sitelib}/*

%changelog
*   Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.3-2
-   BuildRequires and Requires python-babel, python-docutils, python-jinja2,
    python-Pygments, python-six, python-alabaster, python-imagesize,
    python-requests and python-snowballstemmer. Adding python3 version
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.5.3-1
-   Upgrade version to 1.5.3
*   Fri Dec 16 2016 Dheeraj Shetty <dheerajs@vmware.com> 1.5.1-1
-   Initial
