%define srcname sphinxcontrib-applehelp

Name:           python3-sphinxcontrib-applehelp
Version:        1.0.2
Release:        4%{?dist}
Summary:        Sphinx extension for Apple help books
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
URL:            https://pypi.org/project/sphinxcontrib-applehelp
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/9f/01/ad9d4ebbceddbed9979ab4a89ddb78c9760e74e6757b1880f1b2760e8295/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=1325ac83ff15dd28d6f2791caf64e6c08d1dd2f0946dc8891f5c4d8fd062a1e8650c9c39a7459195ef41f3b425f5b8d6c5e277ea85621a36dd870ca5162508da

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-applehelp is a sphinx extension which outputs Apple help books.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.2-4
- Release bump for SRP compliance
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-3
- Fix summary & description
* Mon Nov 28 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.2-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-1
- Initial version
