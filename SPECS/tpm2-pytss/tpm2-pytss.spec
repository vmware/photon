Name:       tpm2-pytss
Version:    1.2.0
Release:    4%{?dist}
Summary:    Python bindings for tpm2-tss
URL:        https://github.com/tpm2-software/tpm2-pytss
Vendor:     VMware, Inc.
Group:      System Environment/Security
Distribution: Photon

Source0: https://github.com/tpm2-software/tpm2-pytss/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pkgconfig
BuildRequires: python3-pycparser
BuildRequires: python3-pip
BuildRequires: python3-wheel
BuildRequires: python3-packaging
BuildRequires: python3-asn1crypto
BuildRequires: python3-cryptography
BuildRequires: python3-setuptools
BuildRequires: python3-setuptools_scm
BuildRequires: python3-typing-extensions
BuildRequires: git
BuildRequires: tpm2-tss-devel

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-cryptography
BuildRequires: python3-cffi
BuildRequires: python3-pip
BuildRequires: python3-PyYAML
%endif

Requires: tpm2-tss
Requires: python3

%description
TPM2 TSS Python bindings for Enhanced System API (ESYS).
This package primarily exposes the TPM 2.0 Enhanced System API.

%prep
%autosetup -p1 -Sgit

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%pytest
%endif

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.2.0-4
- Release bump for SRP compliance
* Fri Jun 28 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.2.0-3
- Fixed build requires to do offline build
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.2.0-2
- Update release to compile with python 3.11
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-1
- First build. Needed for tpm2-pkcs11.
