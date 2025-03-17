%global debug_package %{nil}

Summary:        scp module for paramiko
Name:           python3-scp
Version:        0.14.4
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/scp
Source0:        https://files.pythonhosted.org/packages/05/e0/ac4169e773e12a08d941ca3c006cb8c91bee9d6d80328a15af850b5e7480/scp-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
BuildRequires:  python3-paramiko

Requires:       python3
Requires:       python3-libs
Requires:       python3-paramiko

%description
The scp.py module uses a paramiko transport to send and recieve files via the scp1 protocol.
This is the protocol as referenced from the openssh scp program, and has only been tested with this implementation.

%prep
%autosetup -n scp-%{version}

%build
%py3_build

%install
%py3_install

%check

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.14.4-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.14.4-1
- Automatic Version Bump
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 0.13.3-1
- Automatic Version Bump
* Wed Aug 12 2020 Tapas Kundu <tkundu@vmware.com> 0.13.2-1
- Initial packaging for Photon
