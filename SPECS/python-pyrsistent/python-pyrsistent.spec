%global build_if %{photon_subrelease} >= 92

Summary:        Persistent/Functional/Immutable data structures
Name:           python3-pyrsistent
Version:        0.21.0
Release:        1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pyrsistent
Source0:        https://github.com/tobgu/pyrsistent/archive/refs/tags/v%{version}.tar.gz#/pyrsistent-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging
BuildRequires:  python3-xml
BuildRequires:  python3-hypothesis
BuildRequires:  python3-attrs
BuildRequires:  python3-sortedcontainers
Requires:       python3-attrs
Requires:       python3
Requires:       python3-libs

%description
Pyrsistent is a number of persistent collections (by some referred to as functional data structures).
Persistent in the sense that they are immutable.

All methods on a data structure that would normally mutate it instead return a new copy of the structure containing the requested updates.
The original structure is left untouched.

This will simplify the reasoning about what a program does since no hidden side effects ever can take place to these data structures.
You can rest assured that the object you hold a reference to will remain the same throughout its lifetime and need not worry that
somewhere five stack levels below you in the darkest corner of your application someone has decided to remove that element that you expected to be there.

Pyrsistent is influenced by persistent data structures such as those found in the standard library of Clojure.
The data structures are designed to share common elements through path copying. It aims at taking these concepts
and make them as pythonic as possible so that they can be easily integrated into any python program without hassle.

%prep
%autosetup -n pyrsistent-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%check
python3 setup.py test

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Tue Oct 13 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.21.0-1
- Upgrade to 0.21.0
* Tue Sep 22 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.18.1-5
- Remove stale python3-six dependency
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.18.1-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.18.1-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.18.1-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.18.1-1
- Automatic Version Bump
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.17.3-2
- Fix build with new rpm
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.17.3-1
- Automatic Version Bump
* Thu Jul 30 2020 Tapas Kundu <tkundu@vmware.com> 0.16.0-1
- Initial packaging for Photon
