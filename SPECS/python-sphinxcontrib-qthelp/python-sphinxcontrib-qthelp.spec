%define srcname sphinxcontrib-qthelp

Name:           python3-sphinxcontrib-qthelp
Version:        1.0.3
Release:        4%{?dist}
Summary:        Sphinx extension for QtHelp documents
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
URL:            https://pypi.org/project/sphinxcontrib-qthelp
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/b1/8e/c4846e59f38a5f2b4a0e3b27af38f2fcf904d4bfd82095bf92de0b114ebd/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-qthelp is a sphinx extension which outputs QtHelp document.

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.3-4
- Release bump for SRP compliance
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.3-3
- Fix summary & description
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.3-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.3-1
- initial version
