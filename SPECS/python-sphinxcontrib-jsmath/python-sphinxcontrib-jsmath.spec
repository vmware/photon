Name:           python3-sphinxcontrib-jsmath
Version:        1.0.1
Release:        2%{?dist}
Summary:        A platform independent file lock
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/sphinxcontrib-jsmath
Source0:        https://files.pythonhosted.org/packages/b2/e8/9ed3830aeed71f17c026a07a5097edcf44b692850ef215b161b8ad875729/sphinxcontrib-jsmath-%{version}.tar.gz
%define sha512  sphinxcontrib-jsmath=c1e6488f5c0ca4567c27ec7c597c9db321ac32ce354c4ad62fea534b2ae1c0acb183a921f46216bbc3891f14acfaac05ddf324b8fdaf99828df07bc91aa7e5c7
BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides: python%{python3_version}dist(sphinxcontrib-jsmath)

%description
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%prep
%autosetup -p1 -n sphinxcontrib-jsmath-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} test.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib/

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.1-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-1
- initial version
