%global build_if %{photon_subrelease} >= 92

%define srcname requests-unixsocket

Name:           python3-requests-unixsocket
Version:        0.4.1
Release:        1%{?dist}
Summary:        Use requests to talk HTTP via a UNIX domain socket
Url:            https://pypi.org/project/requests-unixsocket
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/msabramo/requests-unixsocket/archive/refs/tags/v%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-setuptools_scm
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging
BuildRequires: python3-requests
BuildRequires: python3-pip

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires: python3
Requires: python3-requests >= 2.28.1-7

BuildArch: noarch

%description
Requests is an Apache2 Licensed HTTP library, written in Python, for human
beings.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
pip3 install pep8 pytest-cache pytest-pep8 waitress
python3 -m pytest -v
%endif

%clean
rm -rf %{buildroot}/*

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Oct 14 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.4.1-1
- Upgrade to 0.4.1
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.3.0-6
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.0-5
- Bump version as a part of python3.14 upgrade
* Tue Jan 28 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.0-4
- Fix functionality break introduced by CVE-2024-35195 in python3-requests
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.0-3
- Release bump for SRP compliance
* Mon Jun 03 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.0-2
- Use system provided packages to do offline build
* Thu Aug 11 2022 Tapas Kundu <tkundu@vmware.com> 0.3.0-1
- Initial addition
