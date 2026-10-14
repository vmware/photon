%global build_if %{photon_subrelease} >= 92

Summary:        A Universal Character Encoding Detector in Python
Name:           python3-chardet
Version:        7.6.0
Release:        1%{?dist}
Url:            https://github.com/chardet/chardet
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/chardet/chardet/archive/refs/tags/%{version}.tar.gz#/chardet-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3

BuildArch:      noarch

%description
chardet is a universal character encoding detector in Python.

%prep
%autosetup -p1 -n chardet-%{version}

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
PYTHONPATH=%{buildroot}%{python3_sitelib} %pytest -v
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/chardetect

%changelog
* Wed Oct 14 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.6.0-1
- Upgrade to 7.6.0
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.0.0-5
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.0.0-4
- Bump version as a part of python3.14 upgrade
* Mon Jul 28 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.0.0-3
- Clean up unintended licenses
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.0.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 5.0.0-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.0.0-1
- Add python3-setuptools to Requires
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.0.4-2
- Mass removal python2
* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 3.0.4-1
- Initial packaging.
