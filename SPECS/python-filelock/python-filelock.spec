%global build_if %{photon_subrelease} >= 92

Name:           python3-filelock
Version:        3.32.7
Release:        1%{?dist}
Summary:        A platform independent file lock
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/tox-dev/filelock
Source0: https://github.com/tox-dev/filelock/archive/refs/tags/%{version}.tar.gz#/filelock-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging

Requires:       python3

Provides: python%{python3_version}dist(filelock)

%description
This package contains a single module, which implements a platform independent
file locking mechanism for Python.

The lock includes a lock counter and is thread safe. This means, when locking
the same lock object twice, it will not block.

%prep
%autosetup -p1 -n filelock-%{version}

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%check
%{__python3} test.py

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{python3_sitelib}/*

%changelog
* Tue Oct 20 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.32.7-1
- Upgrade to 3.32.7
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.8.0-5
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.8.0-4
- Bump version as a part of python3.14 upgrade
* Wed Feb 11 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 3.8.0-3
- Fix CVE-2026-22701
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.8.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 3.8.0-1
- Automatic Version Bump
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.0.12-1
- initial version
