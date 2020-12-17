%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-filelock
Version:        3.0.12
Release:        1%{?dist}
Summary:        A platform independent file lock
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/benediktschmitt/py-filelock
Source0:        https://files.pythonhosted.org/packages/14/ec/6ee2168387ce0154632f856d5cc5592328e9cf93127c5c9aeca92c8c16cb/filelock-%{version}.tar.gz
%define sha1    filelock=ca03bf213ee1d7a9b6353cebc265072aae40fdcb
BuildArch:      noarch

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3

Requires:       python3

Provides: python3.9dist(filelock)

%description
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%prep
%autosetup -p1 -n filelock-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%check
%{__python3} test.py

%files -n python3-filelock
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{python3_sitelib}/filelock.py
%{python3_sitelib}/filelock-%{version}-py%{python3_version}.egg-info
%exclude %{python3_sitelib}/__pycache__/filelock*.py[co]

%changelog
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.0.12-1
- initial version
