%global build_if %{photon_subrelease} >= 91

Name:           python3-charset-normalizer
Version:        3.5.2
Release:        2%{?dist}
Summary:        The Real First Universal Charset Detector
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/jawah/charset_normalizer

Source0: https://github.com/jawah/charset_normalizer/archive/refs/tags/%{version}.tar.gz#/charset-normalizer-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging

BuildArch:      noarch

%description
A library that helps you read text from an unknown charset encoding.
Motivated by chardet, trying to resolve the issue by taking
a new approach. All IANA character set names for which the Python core
library provides codecs are supported.

%prep
%autosetup -p1 -n charset_normalizer-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
%pytest
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{_bindir}/normalizer
%{python3_sitelib}/*

%changelog
* Wed Nov 04 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.5.2-2
- extend release to 91
* Thu Oct 29 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.5.2-1
- Upgrade to 3.5.2
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.1.1-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.1.1-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.1.1-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.1-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.0.9-1
- Initial verision, needed for python3-requests-2.26.0
