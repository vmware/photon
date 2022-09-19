Name:           python3-sphinxcontrib-devhelp
Version:        1.0.2
Release:        2%{?dist}
Summary:        A platform independent file lock
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/sphinxcontrib-devhelp
Source0:        https://files.pythonhosted.org/packages/98/33/dc28393f16385f722c893cb55539c641c9aaec8d1bc1c15b69ce0ac2dbb3/sphinxcontrib-devhelp-%{version}.tar.gz
%define sha512  sphinxcontrib-devhelp=83b46eaf26df3932ea2136cfda1c0fca4fc08ce8bca564845b3efe5bb00d6c8c93991f4edd4913d4ec796e2d85bd2c7265adf28e98f42e8094daeb5ac11a0eb1
BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides: python%{python3_version}dist(sphinxcontrib-devhelp)

%description
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%prep
%autosetup -p1 -n sphinxcontrib-devhelp-%{version}
find -name '*.mo' -delete

%build
%py3_build

%install
%py3_install

%check
%{_python3} test.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%license LICENSE
%doc README.rst

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.2-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-1
- initial version
