%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-resolvelib
Version:        0.5.5
Release:        1%{?dist}
Summary:        Resolve abstract dependencies into concrete ones
License:        ISC
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/sarugaku/resolvelib
Source0:        https://github.com/sarugaku/resolvelib/archive/refs/tags/resolvelib-%{version}.tar.gz
%define sha1    resolvelib=63f6622d740a6abc6d0bb906c901cdf1ca550a70
BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides: python3.9dist(resolvelib)

%description
Resolve abstract dependencies into concrete ones
ResolveLib at the highest level provides a Resolver class that includes
dependency resolution logic.
You give it some things, and a little information on how it should interact
with them, and it will spit out a resolution result.

%prep
%autosetup -p1 -n resolvelib-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%check
%{__python3} test.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%license LICENSE
%doc README.rst
%{python3_sitelib}/resolvelib

%changelog
* Wed Jun 02 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.5.5-1
- Initial version
