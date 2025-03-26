%define srcname sphinxcontrib-serializinghtml

Name:           python3-sphinxcontrib-serializinghtml
Version:        1.1.5
Release:        3%{?dist}
Summary:        Sphinx extension for serialized HTML
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/sphinxcontrib-serializinghtml

Source0: https://files.pythonhosted.org/packages/ac/86/021876a9dd4eac9dae0b1d454d848acbd56d5574d350d0f835043b5ac2cd/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-serializinghtml is a sphinx extension which outputs "serialized"
HTML files (json and pickle).

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%license LICENSE
%doc README.rst

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.1.5-3
- Release bump for SRP compliance
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.5-2
- Fix summary & description
* Mon Sep 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.5-1
- Upgrade to v1.1.5
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-1
- initial version
