Summary:        autopep8 automatically formats Python code
Name:           python3-autopep8
Version:        2.0.0
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/python-autopep8/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        autopep8-%{version}.tar.gz
%define sha512 autopep8=883b79f7011a374a2ef88073a45748268a20449a3bc8da519c036c71700352dd8c4accc60fcb592f1a53ceac06984fcbe6ede8a272bc718c2b79873be5f35dd8

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-toml

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-tools
BuildRequires: python3-pycodestyle
%endif

Requires:       python3-toml
Requires:       python3
Requires:       python3-pycodestyle
Requires:       python3-tools

%description
autopep8 automatically formats Python code to conform to the PEP 8 style guide.
It uses the pycodestyle utility to determine what parts of the code needs to be
formatted.

%prep
%autosetup -p1 -n autopep8-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
%pytest -v
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/autopep8

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.0-3
- Release bump for SRP compliance
* Thu Aug 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.0-2
- Fix requires
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.0-1
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
- Automatic Version Bump
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.5.4-2
- Add python3-toml to requires
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.4-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.3-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.4.4-2
- Mass removal python2
* Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> 1.4.4-1
- Initial packaging for Photon
