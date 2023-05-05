Name:           python3-portalocker
Version:        2.7.0
Release:        1%{?dist}
Summary:        An easy library for Python file locking.
License:        BSD-3-Clause
Group:          Development/Languages/Python
Url:            https://github.com/WoLpH/portalocker
Source0:        https://files.pythonhosted.org/packages/1f/f8/969e6f280201b40b31bcb62843c619f343dcc351dff83a5891530c9dd60e/portalocker-2.7.0.tar.gz
%define sha512  portalocker=9f6dc31fda36f2fcc7088134b5249c6ec4a92a1fa2e85bf55c700469f183d29ed1a1bd522b65909844c85dfe6872d83809d21b78dc89886533db2692cc709ed2
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3

BuildArch:      noarch

%description
Portalocker is a library to provide an easy API to file locking.
An important detail to note is that on Linux and Unix systems the locks are advisory by default. By specifying the -o mand option to the mount command it is possible to enable mandatory file locking on Linux. This is generally not recommended however.

%prep
%autosetup -n portalocker-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
%pytest

%files
%{python3_sitelib}/*

%changelog
* Mon May 01 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2.7.0-1
- Initial Build. Required by python-ConcurrentLogHandler
