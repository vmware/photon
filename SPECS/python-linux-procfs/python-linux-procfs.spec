%global build_if %{photon_subrelease} >= 91

#
# spec file for package python3-linux-procfs
#

Name:           python3-linux-procfs
Version:        0.7.4
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Summary:        Linux /proc abstraction classes
URL:            https://git.kernel.org/pub/scm/libs/python/python-linux-procfs/python-linux-procfs.git/

BuildArch:     noarch

Source0:        https://cdn.kernel.org/pub/software/libs/python/python-linux-procfs/python-linux-procfs-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-build
BuildRequires: python3-setuptools
BuildRequires: python3-installer
BuildRequires: python3-packaging

Requires:      python3

%description
Abstractions to extract information from the Linux kernel /proc files.

%prep
%autosetup -n python-linux-procfs-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%check
LANG=en_US.UTF-8 python3 bitmasklist_test.py

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{_bindir}/pflags
%{python3_sitelib}/*
%license COPYING

%changelog
* Wed Nov 04 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.7.4-2
- extend release to 91
* Wed Oct 07 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.7.4-1
- Upgrade to 0.7.4
* Mon May 18 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 0.7.0-5
- Remove deprecated python3-defusedxml from BuildRequires
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.7.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.7.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.7.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.7.0-1
- Automatic Version Bump
* Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.6.1-1
- Initial version.
