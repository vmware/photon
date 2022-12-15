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
%define sha512  resolvelib=3da39201c4472d45466750119282fc34591b6d79eb4e6e71ca3f221e43dceead213058b4b72bee00083e9885650a47486bd7496264fba10f623aec7c19dabf00
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides:       python%{python_version}(resolvelib)

%description
Resolve abstract dependencies into concrete ones
ResolveLib at the highest level provides a Resolver class that includes
dependency resolution logic.
You give it some things, and a little information on how it should interact
with them, and it will spit out a resolution result.

%prep
%autosetup -p1 -n resolvelib-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} test.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Dec 15 2022 Nitesh Kumar <kunitesh@vmware.com> 0.5.5-1
- Initial version, needed for ansible-2.11.12
