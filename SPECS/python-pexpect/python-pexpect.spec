Summary:        Pexpect is a Pure Python Expect-like module
Name:           python3-pexpect
Version:        4.8.0
Release:        4%{?dist}
License:        ISC
Url:            https://github.com/pexpect/pexpect
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/pexpect/pexpect/archive/pexpect-%{version}.tar.gz
%define sha512  pexpect=7447ae2d1e13be422c894a8fd51c5aaa788e37ea7f0c798c88b77afd401fb3631400a637077ccbb83c2e3876b0d0c5e1dbd5fdc9d3739d785b4d5ad7c0192580

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  man-db
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-pytest
BuildRequires:  python3-attrs
BuildRequires:  python3-ptyprocess
BuildRequires:  python3-xml
%endif

Requires:       python3
Requires:       python3-ptyprocess

BuildArch:      noarch

%description
Pexpect is a pure Python module for spawning child applications; controlling them;
and responding to expected patterns in their output. Pexpect works like Don Libes Expect.
Pexpect allows your script to spawn a child application and control it as if a human
were typing commands.

%prep
%autosetup -n pexpect-%{version}

%build
%py3_build

%install
%py3_install

%files
%{python3_sitelib}/*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.8.0-4
- Bump version as a part of openssl upgrade
* Mon Nov 28 2022 Prashant S Chauhan <psinghchauha@vmware.com> 4.8.0-3
- Update release to compile with python 3.11
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.8.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 4.8.0-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 4.6.0-4
- Mass removal python2
* Mon Sep 09 2019 Tapas Kundu <tkundu@vmware.com> 4.6.0-3
- Fix make check
* Wed Dec 05 2018 Ashwin H <ashwinh@vmware.com> 4.6.0-2
- Add %check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.6.0-1
- Update to version 4.6.0
* Tue Sep 19 2017 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-2
- Adding requires on ptyprocess
* Mon Sep 11 2017 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-1
- Initial packaging for Photon
