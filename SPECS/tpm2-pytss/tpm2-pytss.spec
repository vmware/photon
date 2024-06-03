Name:       tpm2-pytss
Version:    2.2.1
Release:    1%{?dist}
Summary:    Python bindings for tpm2-tss
License:    BSD
URL:        https://github.com/tpm2-software/tpm2-pytss
Vendor:     VMware, Inc.
Group:      System Environment/Security
Distribution: Photon

Source0: https://github.com/tpm2-software/tpm2-pytss/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=b55c8f0ba03204e803e33da115961893a1a7e08bcac29399a728d9f984be2d538076fa7dd289e96beedb6d6125a53f5b5841dd216f89d55833db9eb9197ba747

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-setuptools_scm
BuildRequires: python3-packaging
BuildRequires: python3-pkgconfig
BuildRequires: python3-pycparser
BuildRequires: git
BuildRequires: tpm2-tss-devel
BuildRequires: python3-pip
BuildRequires: python3-wheel
BuildRequires: python3-cffi
BuildRequires: python3-asn1crypto

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-cryptography
BuildRequires: python3-cffi
BuildRequires: python3-PyYAML
%endif

Requires: tpm2-tss
Requires: python3
Requires: python3-cffi
Requires: python3-asn1crypto

%description
TPM2 TSS Python bindings for Enhanced System API (ESYS).
This package primarily exposes the TPM 2.0 Enhanced System API.

%prep
%autosetup -p1 -Sgit

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%pytest

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Tue Jun 04 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.2.1-1
- Upgrade to v2.2.1
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.2.0-2
- Update release to compile with python 3.11
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-1
- First build. Needed for tpm2-pkcs11.
