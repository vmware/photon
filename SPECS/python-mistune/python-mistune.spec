%global build_if %{photon_subrelease} >= 91

%define srcname mistune

Summary:        The fastest markdown parser in pure Python.
Name:           python3-mistune
Version:        3.2.0
Release:        3%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/mistune

Source0: https://files.pythonhosted.org/packages/source/m/mistune/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2026-33079.patch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-pip
%endif

Requires: python3

BuildArch: noarch

%description
The fastest markdown parser in pure Python with renderer features, inspired by marked.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
pip3 install tomli
%{pytest}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Jun 16 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.2.0-3
- Fix CVE-2026-33079
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.2.0-2
- Extended to build for subrelease 91 and above
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.2.0-1
- Version upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.5-2
- Release bump for SRP compliance
* Sun Aug 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.5-1
- Upgrade to v2.0.5
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.4-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.4-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.4-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.8.3-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.8.3-1
- Update to version 0.8.3
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-1
- Initial packaging for Photon
