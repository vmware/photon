Name:           python3-resolvelib
Version:        0.8.1
Release:        2%{?dist}
Summary:        Resolve abstract dependencies into concrete ones
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/sarugaku/resolvelib
Source0:        https://github.com/sarugaku/resolvelib/archive/refs/tags/resolvelib-%{version}.tar.gz
%define sha512  resolvelib=4e1a7d84ee3fb86433701562aff71d0c867428f2bcb58ce998aee13896945b54a0915540dea7dcc3fd1e2544b43ef276df8a1804cbbc9330936169bef98a1c5d

Source1: license.txt
%include %{SOURCE1}
BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides: python%{python3_version}dist(resolvelib)

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
%license LICENSE
%doc README.rst
%{python3_sitelib}/resolvelib

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.8.1-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.8.1-1
- Automatic Version Bump
* Wed Jun 02 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.5.5-1
- Initial version
