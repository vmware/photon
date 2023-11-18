Summary:        Pygments is a syntax highlighting package written in Python.
Name:           python3-Pygments
Version:        2.13.0
Release:        3%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Pygments

Source0: https://files.pythonhosted.org/packages/source/P/Pygments/Pygments-%{version}.tar.gz
%define sha512 Pygments=d492acf112423fa997f35d6d3cae18b89bf11619c696879c6df49697dca933b6d54d7cb22907e06812e0a562f03e8ed5ccefde5247bc1c51cf2d3d69e7d65422

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif

Requires:       python3
Requires:       python3-setuptools

BuildArch:      noarch

%description
Pygments is a syntax highlighting package written in Python.
It is a generic syntax highlighter suitable for use in code hosting, forums, wikis or other applications that need to prettify source code. Highlights are:
a wide range of over 300 languages and other text formats is supported
special attention is paid to details, increasing quality by a fair amount
support for new languages and formats are added easily
a number of output formats, presently HTML, LaTeX, RTF, SVG, all image formats that PIL supports and ANSI sequences
it is usable as a command-line tool and as a library.

%prep
%autosetup -n Pygments-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.13.0-3
- Bump version as a part of openssl upgrade
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
