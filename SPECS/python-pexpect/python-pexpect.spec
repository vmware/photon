Summary:        Pexpect is a Pure Python Expect-like module
Name:           python3-pexpect
Version:        4.8.0
Release:        3%{?dist}
License:        ISC
Url:            https://github.com/pexpect/pexpect
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/pexpect/pexpect/archive/pexpect-%{version}.tar.gz
%define sha1    pexpect=ee5dd435ca68dc05daa783e3330eea365a404378

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  man-db
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-pytest
BuildRequires:  python3-attrs
BuildRequires:  python3-ptyprocess
BuildRequires:  python3-xml
BuildRequires:  python3-pip
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-ptyprocess

BuildArch:      noarch

%description
Pexpect is a pure Python module for spawning child applications; controlling them;
and responding to expected patterns in their output. Pexpect works like Don Libes Expect.
Pexpect allows your script to spawn a child application and control it as if a human
were typing commands.

%prep
%autosetup -p1 -n pexpect-%{version}

%build
python3 setup.py build

%install
rm -rf %{buildroot}
python3 setup.py install --root=%{buildroot}

%check
pip3 install pathlib2 funcsigs pluggy more_itertools
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python3_sitelib} \
py.test3

%files
%{python3_sitelib}/*

%changelog
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 4.8.0-3
-   Update release to compile with python 3.10
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.8.0-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 4.8.0-1
-   Automatic Version Bump
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 4.6.0-4
-   Mass removal python2
*   Mon Sep 09 2019 Tapas Kundu <tkundu@vmware.com> 4.6.0-3
-   Fix make check
*   Wed Dec 05 2018 Ashwin H <ashwinh@vmware.com> 4.6.0-2
-   Add %check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.6.0-1
-   Update to version 4.6.0
*   Tue Sep 19 2017 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-2
-   Adding requires on ptyprocess
*   Mon Sep 11 2017 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-1
-   Initial packaging for Photon
