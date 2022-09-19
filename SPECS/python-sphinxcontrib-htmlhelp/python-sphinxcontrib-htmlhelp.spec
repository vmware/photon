Name:           python3-sphinxcontrib-htmlhelp
Version:        2.0.0
Release:        2%{?dist}
Summary:        A platform independent file lock
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/sphinxcontrib-htmlhelp

Source0: https://files.pythonhosted.org/packages/eb/85/93464ac9bd43d248e7c74573d58a791d48c475230bcf000df2b2700b9027/sphinxcontrib-htmlhelp-%{version}.tar.gz
%define sha512 sphinxcontrib-htmlhelp=6ed673966615f3e818e00de4b7e59c27f0a0d7b494294f804540777c580480870c36002c08d8ad626b7b41a676fe40edc0b0b5ffc6ad8080f38f59c24e157636

%if 0%{?with_check}
Patch0: fix-tests.patch
%endif

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

%if 0%{?with_check}
BuildRequires: python3-sphinx
BuildRequires: python3-pytest
BuildRequires: python3-pip
%endif

Requires: python3

Provides: python%{python3_version}dist(sphinxcontrib-htmlhelp)

%description
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%prep
%autosetup -p1 -n sphinxcontrib-htmlhelp-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
pip3 install html5lib
%pytest
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib/

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.0-2
- Update release to compile with python 3.11
* Mon Sep 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.0-1
- Upgrade to v2.0.0
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.3-1
- initial version
