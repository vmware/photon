%global build_if %{photon_subrelease} >= 91

Name:       tpm2-pytss
Version:    2.3.0
Release:    2%{?dist}
Summary:    Python bindings for tpm2-tss
URL:        https://github.com/tpm2-software/tpm2-pytss
Vendor:     VMware, Inc.
Group:      System Environment/Security
Distribution: Photon

Source0: https://github.com/tpm2-software/tpm2-pytss/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: replace-asn1crypto-with-the-ASN.1-parser-in-cryptography.patch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pkgconfig
BuildRequires: python3-pycparser
BuildRequires: python3-wheel
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging
BuildRequires: python3-cryptography
BuildRequires: python3-setuptools
BuildRequires: python3-setuptools_scm
BuildRequires: python3-typing-extensions
BuildRequires: tpm2-tss-devel

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-cffi
BuildRequires: python3-pip
BuildRequires: python3-PyYAML
%endif

Requires: tpm2-tss
Requires: python3
Requires: python3-cryptography

%description
TPM2 TSS Python bindings for Enhanced System API (ESYS).
This package primarily exposes the TPM 2.0 Enhanced System API.

%prep
%autosetup -p1

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%pytest
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Nov 04 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.3.0-2
- extend release to 91
* Thu Jun 04 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.3.0-1
- Upgrade to latest as part of cryptography & python3 upgrade
* Thu May 21 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.2.0-7
- Replace asn1crypto with stdlib base64 + minimal DER helpers in tsskey.py
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.2.0-6
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.2.0-5
- Bump version as a part of python3.14 upgrade
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.2.0-4
- Release bump for SRP compliance
* Fri Jun 28 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.2.0-3
- Fixed build requires to do offline build
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.2.0-2
- Update release to compile with python 3.11
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-1
- First build. Needed for tpm2-pkcs11.
