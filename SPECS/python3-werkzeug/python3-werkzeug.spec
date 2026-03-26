%global build_if %{photon_subrelease} >= 92
%define srcname werkzeug

Summary:        The Swiss Army knife of Python web development
Name:           python3-werkzeug
Version:        3.1.7
Release:        1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Werkzeug

BuildArch:      noarch

Source0: https://github.com/pallets/werkzeug/releases/download/%{version}/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-flit-core

%if 0%{?with_check}
BuildRequires:  python3-requests
BuildRequires:  python3-cffi
BuildRequires:  python3-cryptography
BuildRequires:  python3-markupsafe
BuildRequires:  python3-pytest
BuildRequires:  python3-pluggy
BuildRequires:  python3-hypothesis
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif

Requires:       python3

%description
Werkzeug started as simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility modules. It includes a powerful debugger, full featured request and response objects, HTTP utilities to handle entity tags, cache control headers, HTTP dates, cookie handling, file uploads, a powerful URL routing system and a bunch of community contributed addon modules.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%if 0%{?with_check}
%check
pip3 install ephemeral-port-reserve watchdog pytest-timeout
# these tests get hung
rm tests/middleware/test_http_proxy.py \
   tests/test_debug.py \
   tests/test_serving.py
%pytest
%endif

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Thu Mar 26 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1.7-1
- Upgrade to v3.1.7
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.2-5
- Bump version as a part of python3.14 upgrade
* Tue Apr 1 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.2-4
- Fix CVE-2024-49767, CVE-2023-25577, CVE-2023-23934, CVE-2023-46136
* Wed Dec 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.2-3
- Fix CVE-2024-34069
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.2-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.2-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-3
- Bump version as a part of requests & chardet upgrade
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.1-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.14.1-3
- Mass removal python2
* Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> 0.14.1-2
- Fix make check
- Moved buildrequires from subpackage
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.14.1-1
- Update to version 0.14.1
* Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 0.12.1-2
- Fixed rpm check errors
* Thu Mar 30 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.12.1-1
- Updating package to latest
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.11.15-1
- Initial packaging for Photon.
