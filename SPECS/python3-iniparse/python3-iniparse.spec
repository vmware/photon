%global build_if %{photon_subrelease} >= 91

Name:           python3-iniparse
Version:        0.5.1
Release:        2%{?dist}
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
Group:          Development/Libraries
URL:            http://code.google.com/p/iniparse/
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0:        http://iniparse.googlecode.com/files/iniparse-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging

%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-test
%endif

Requires:       python3
Requires:       python3-pycparser

%description
iniparse is an INI parser for Python which is API compatible
with the standard library's ConfigParser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.

%prep
%autosetup -p1 -n python-iniparse-%{version}

%build
%py3_build_wheel

%install
%{py3_install_wheel}
rm -r %{buildroot}%{_docdir}
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
rm tests/test_multiprocessing.py
%pytest
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.5.1-2
- Extended to build for subrelease 91 and above
* Sat Mar 28 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.5.1-1
- Upgrade to v0.5.1
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.5-4
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.5-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.5-2
- Update release to compile with python 3.11
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.5-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.4-7
- Mass removal python2
* Tue Jul 11 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4-6
- Fix python3 and make check issues.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.4-5
- Use python2 explicitly to build
* Mon May 22 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4-4
- Added python3 subpackage.
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 0.4-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.4-2
- GA - Bump release of all rpms
* Sat Jun 12 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.4-1
- Release 0.4
* Sat Apr 17 2010 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.2-1
- Release 0.3.2
* Mon Mar 2 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.1-1
- Release 0.3.1
* Fri Feb 27 2009 Paramjit Oberoi <param@cs.wisc.edu> - 0.3.0-1
- Release 0.3.0
* Sat Dec 6 2008 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.4-1
- Release 0.2.4
- added egg-info file to %%files
* Tue Dec 11 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.3-1
- Release 0.2.3
* Mon Sep 24 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.2-1
- Release 0.2.2
* Tue Aug 7 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.1-1
- Release 0.2.1
* Fri Jul 27 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-3
- relocated doc to %{_docdir}/python-iniparse-%{version}
* Thu Jul 26 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-2
- changed name from iniparse to python-iniparse
* Tue Jul 17 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-1
- Release 0.2
- Added html/* to %%doc
* Fri Jul 13 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.1-1
- Initial build.
