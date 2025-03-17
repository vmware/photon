Summary:        Pure Python netlink library
Name:           python3-pyroute2
Version:        0.7.3
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/svinota/pyroute2
Source0:        https://pypi.io/packages/source/p/pyroute2/pyroute2-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  git
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-xml
BuildArch:      noarch

%description
The pyroute2 library consists of a common netlink messages coder / decoder
and a number of protocol-specific modules. It may be used to work with
existing protocols such as RTNL as well as to create your own netlink protocols.

%prep
%autosetup -n pyroute2-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/ss2
%{_bindir}/pyroute2-cli
%{_bindir}/pyroute2-test-platform
%{_bindir}/pyroute2-dhcp-client
%doc README* LICENSE.Apache* LICENSE.GPL*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.7.3-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.7.3-1
- Update to 0.7.3
* Wed Apr 07 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.5.17-1
- Initial Packaging for pyroute2
