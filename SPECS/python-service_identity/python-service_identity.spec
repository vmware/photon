%global build_if %{photon_subrelease} >= 91

%define srcname service-identity

Summary:        Service identity verification for pyOpenSSL.
Name:           python3-service_identity
Version:        26.1.0
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/%{srcname}

BuildArch:      noarch

Source0: https://github.com/pyca/service-identity/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: 0001-Remove-coverage-toml-test-dependency.patch
Patch1: 0002-Remove-hatch-fancy-pypi-readme-build-system-dependency.patch

BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-setuptools_scm

%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-cryptography
%endif

Requires:       python3
Requires:       python3-attrs
Requires:       python3-cryptography

%description
%{srcname} aspires to give you all the tools you need for verifying whether a certificate is valid for the intended purposes.

In the simplest case, this means host name verification. However, %{srcname} implements RFC 6125 fully and plans to add other relevant RFCs too.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build_wheel}

%install
%{py3_install_wheel}
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
%pytest -v
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Nov 04 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 26.1.0-2
- extend release to 91
* Thu Sep 03 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 26.1.0-1
- Upgrade to v26.1.0
- Fix make check
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 21.1.0-5
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 21.1.0-4
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 21.1.0-3
- Release bump for SRP compliance
* Tue Dec 26 2023 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 21.1.0-2
- Bump up as part of python3-pyOpenSSL update
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 21.1.0-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 18.1.0-2
- Mass removal python2
* Mon Jun 01 2020 Tapas Kundu <tkundu@vmware.com> 18.1.0-1
- Update to 18.1.0
* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 17.0.0-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.0.0-1
- Update to version 17.0.0
* Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 16.0.0-3
- Fixed runtime dependencies
- Fixed make check errors
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.0.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 16.0.0-1
- Initial packaging for Photon.
