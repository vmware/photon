Name:           python3-filelock
Version:        3.8.0
Release:        1%{?dist}
Summary:        A platform independent file lock
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/benediktschmitt/py-filelock
Source0:        https://files.pythonhosted.org/packages/14/ec/6ee2168387ce0154632f856d5cc5592328e9cf93127c5c9aeca92c8c16cb/filelock-%{version}.tar.gz
%define sha512  filelock=95fb4d420a316199a658e20f385d5eec9db9398a78803cad581f73efb136d2935308a04b1bcf6cebd71a8601f72d006a491937664ec0b70904c305c5796a4bf1
BuildArch:      noarch

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3

Requires:       python3

Provides: python%{python3_version}dist(filelock)

%description
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%prep
%autosetup -p1 -n filelock-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} test.py

%files -n python3-filelock
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{python3_sitelib}/filelock/*
%{python3_sitelib}/filelock-0.0.0-py%{python3_version}.egg-info/*
%exclude %{python3_sitelib}/filelock/__pycache__/filelock*.py[co]

%changelog
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 3.8.0-1
- Automatic Version Bump
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.0.12-1
- initial version
