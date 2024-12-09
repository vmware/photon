Summary:        The code coverage tool for Python
Name:           python3-coverage
Version:        6.4.4
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/coverage
Source0:        https://files.pythonhosted.org/packages/source/c/coverage/coverage-%{version}.tar.gz
%define sha512  coverage=f210f2471b170e05d4dac2cc9a91e3f0d4ba6456cdf91dc1c0ef67a02a11f4279c5beca5df8854c42660346995492b1eff020e1ac578d2a0a129627dadd17114

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  iana-etc
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-six
%endif

%description
Code coverage measurement for Python.
Coverage.py measures code coverage, typically during test execution. It uses the code analysis tools and tracing hooks provided in the Python standard library to determine which lines are executable, and which have been executed.

%prep
%autosetup -n coverage-%{version}

%build
%py3_build

%install
%py3_install

%check
LANG=en_US.UTF-8 tox -e py36

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/coverage
%{_bindir}/coverage3
%{_bindir}/coverage-%{python3_version}

%changelog
*   Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.4.4-2
-   Release bump for SRP compliance
*   Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 6.4.4-1
-   Automatic Version Bump
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.3-2
-   openssl 1.1.1
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 5.3-1
-   Automatic Version Bump
*   Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 5.2.1-1
-   Automatic Version Bump
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 4.5.1-3
-   Mass removal python2
*   Mon Oct 21 2019 Shreyas B. <shreyasb@vmware.com> 4.5.1-2
-   Fixed makecheck errors.
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.5.1-1
-   Updated to 4.5.1
*   Thu Aug 10 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.4-5
-   Fixed make check errors
*   Fri Jul 07 2017 Chang Lee <changlee@vmware.com> 4.3.4-4
-   Add python-xml and pyhton3-xml to  Requires.
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.4-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.3.4-2
-   Packaging python2 and oython3 scripts in bin directory
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.4-1
-   Initial packaging for Photon
