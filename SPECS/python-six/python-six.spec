Name:           python-six
Version:        1.9.0
Release:        1%{?dist}
Summary:        Python 2 and 3 compatibility utilities
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/s/six/six-%{version}.tar.gz
Source0:        six-%{version}.tar.gz
%define sha1 six=d168e6d01f0900875c6ecebc97da72d0fda31129

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires: python2
Requires: python2-libs

BuildArch:      noarch

%description
Six is a Python 2 and 3 compatibility library. It provides utility functions for smoothing over the differences between the Python versions with the goal of writing Python code that is compatible on both Python versions. 

%prep
%setup -n six-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
