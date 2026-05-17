%global build_if %{photon_subrelease} >= 91

%define srcname sphinxcontrib_applehelp

Name:           python3-sphinxcontrib-applehelp
Version:        2.0.0
Release:        2%{?dist}
Summary:        Sphinx extension for Apple help books
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
URL:            https://pypi.org/project/sphinxcontrib-applehelp
Distribution:   Photon

BuildArch: noarch

Source0: %{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-setuptools
BuildRequires: python3-flit-core

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-applehelp is a sphinx extension which outputs Apple help books.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.0.0-2
- Extended to build for subrelease 91 and above
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.0-1
- Version upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.2-4
- Release bump for SRP compliance
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-3
- Fix summary & description
* Mon Nov 28 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.2-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-1
- Initial version
