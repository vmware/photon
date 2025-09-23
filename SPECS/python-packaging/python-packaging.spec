Summary:        Core utilities for Python packages
Name:           python3-packaging
Version:        25.0
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/packaging
License:        BSD or ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://files.pythonhosted.org/packages/source/p/packaging/packaging-%{version}.tar.gz
%define sha512  packaging=0672602d2e18c3aee71b3e567b0de572bc8613ee3d24a79a655ded23ac08ec4582193225bc0c0ea390ed81cf5efbb46e8afbe0798d14f2235f811f263c25728c

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core
%if 0%{?with_check}
BuildRequires:  python3-setuptools
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-xml
BuildRequires:  python3-pyparsing
BuildRequires:  python3-six
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-pyparsing
Requires:       python3-six
BuildArch:      noarch

Provides: python%{python3_version}dist(packaging)

%description
Core utilities for Python packages.

%prep
%autosetup -p1 -n packaging-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%if 0%{?with_check}
%check
pip3 install pretend pytest
PYTHONPATH=./ pytest
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Sep 22 2025 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 25.0-1
-   Update to latest as runtime requirement for pyinstaller
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 20.4-4
-   Update release to compile with python 3.10
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 20.4-3
-   Fix build with new rpm
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 20.4-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.4-1
-   Automatic Version Bump
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 17.1-3
-   Mass removal python2
*   Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 17.1-2
-   Fix makecheck
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.1-1
-   Update to version 17.1
*   Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 16.8-4
-   Fixed rpm check errors
-   Fixed runtime dependencies
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 16.8-3
-   Fix arch
*   Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 16.8-2
-   Remove python-setuptools from BuildRequires
*   Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> 16.8-1
-   Initial packaging for Photon
