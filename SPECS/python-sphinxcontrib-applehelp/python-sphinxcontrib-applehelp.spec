Name:           python3-sphinxcontrib-applehelp
Version:        1.0.2
Release:        2%{?dist}
Summary:        A platform independent file lock
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/sphinxcontrib-applehelp
Source0:        https://files.pythonhosted.org/packages/9f/01/ad9d4ebbceddbed9979ab4a89ddb78c9760e74e6757b1880f1b2760e8295/sphinxcontrib-applehelp-%{version}.tar.gz
%define sha512 sphinxcontrib-applehelp=1325ac83ff15dd28d6f2791caf64e6c08d1dd2f0946dc8891f5c4d8fd062a1e8650c9c39a7459195ef41f3b425f5b8d6c5e277ea85621a36dd870ca5162508da
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides: python%{python3_version}dist(sphinxcontrib-applehelp)

%description
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%prep
%autosetup -p1 -n sphinxcontrib-applehelp-%{version}

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
* Mon Nov 28 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.2-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-1
- Initial version
