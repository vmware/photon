%global build_if %{photon_subrelease} >= 92

%define srcname pygments

Summary:        Pygments is a syntax highlighting package written in Python.
Name:           python3-Pygments
Version:        2.19.2
Release:        1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Pygments

BuildArch:      noarch

Source0: https://github.com/pygments/pygments/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# Note: If you are fixing a CVE here, please check for the same in python3-pip

BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-hatchling

Requires:       python3

%description
Pygments is a syntax highlighting package written in Python.
It is a generic syntax highlighter suitable for use in code hosting, forums, wikis or other applications that need to prettify source code. Highlights are:
a wide range of over 300 languages and other text formats is supported
special attention is paid to details, increasing quality by a fair amount
support for new languages and formats are added easily
a number of output formats, presently HTML, LaTeX, RTF, SVG, all image formats that PIL supports and ANSI sequences
it is usable as a command-line tool and as a library.

%prep
%autosetup -p1 -n %{srcname}-%{version}
%if 0%{?with_check} == 0
rm -r tests/examplefiles
%endif

%build
%py3_build_wheel

%install
%py3_install_wheel

%{py_byte_compile_and_ghost}

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Fri Mar 27 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.19.2-1
- Upgrade to v2.19.2
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.13.0-6
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.13.0-5
- Release bump for SRP compliance
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2.13.0-4
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.13.0-3
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.13.0-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.13.0-1
- Automatic Version Bump
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.9.0-1
- Update to 2.9.0, Fixes CVE-2021-20270, CVE-2021-27291
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.7.2-2
- Fix build with new rpm
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.2-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.7.1-2
- openssl 1.1.1
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.6.1-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.4.2-2
- Mass removal python2
* Thu Jun 13 2019 Tapas Kundu <tkundu@vmware.com> 2.4.2-1
- Update to release 2.4.2
* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 2.2.0-3
- Fix makecheck
* Fri Jul 28 2017 Divya Thaluru <dthaluru@vmware.com> 2.2.0-2
- Fixed make check errors
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 2.2.0-1
- Initial packaging for Photon
