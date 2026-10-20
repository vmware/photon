%global build_if %{photon_subrelease} >= 92

%global srcname distlib

Name:           python3-distlib
Version:        0.4.4
Release:        1%{?dist}
Summary:        Low-level components of distutils2/packaging, augmented with higher-level APIs
URL:            https://pypi.org/project/distlib
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pypa/distlib/archive/refs/tags/%{version}.tar.gz#/distlib-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

# Note: If you are fixing a CVE here, please check for the same in python3-pip

BuildRequires:  python3-devel
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging

Requires:       python3

Provides:       python%{python3_version}dist(distlib)

%description
Distlib contains the implementations of the packaging PEPs and other low-level
features which relate to packaging, distribution and deployment of Python
software. If Distlib can be made genuinely useful, then it is possible for
third-party packaging tools to transition to using it. Their developers and
users then benefit from standardised implementation of low-level functions,
time saved by not having to reinvent wheels, and improved interoperability
between tools.

%prep
%autosetup -p1 -n %{srcname}-%{version}

rm -rf distlib/*.exe \
       distlib/_backport

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
export PYTHONHASHSEED=0
%{python3} setup.py test
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Oct 20 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.4.4-1
- Upgrade to 0.4.4
* Thu May 21 2026 Ajay Kaher <ajay.kaher@broadcom.com> 0.3.6-6
- Drop unzip BuildRequires; not needed for tar.gz source
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.3.6-5
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.6-4
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.6-3
- Release bump for SRP compliance
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.3.6-2
- Spec fixes. Remove readme, license files.
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.3.6-1
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.3.1-1
- initial version
