%define srcname Werkzeug

Summary:        The Swiss Army knife of Python web development
Name:           python3-werkzeug
Version:        2.2.2
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Werkzeug

Source0: https://files.pythonhosted.org/packages/f8/c1/1c8e539f040acd80f844c69a5ef8e2fccdf8b442dabb969e497b55d544e1/%{srcname}-%{version}.tar.gz
%define sha512 Werkzeug=b37a63ba1d6970b10ba17b87575c2d030ad6c4c00ab50669d678297b9801e319f4f81f98bfc2d89fc2e645c5e192dd81ed2d653c03dbaef06565de0bdac2bcf7

Patch0: CVE-2024-34069.patch
Patch1: CVE-2023-25577.patch
Patch2: CVE-2024-49767.patch
Patch3: CVE-2023-23934.patch
Patch4: CVE-2023-46136.patch

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

%if 0%{?with_check}
BuildRequires:  python3-requests
BuildRequires:  curl-devel
%endif

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Werkzeug started as simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility modules. It includes a powerful debugger, full featured request and response objects, HTTP utilities to handle entity tags, cache control headers, HTTP dates, cookie handling, file uploads, a powerful URL routing system and a bunch of community contributed addon modules.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
%if 0%{?with_check}
pip3 install pytest hypothesis
LANG=en_US.UTF-8 PYTHONPATH=./ python3 setup.py test
%endif

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Tue Apr 1 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.2-2
- Fix CVE-2024-49767, CVE-2023-25577, CVE-2023-23934 & CVE-2023-46136
* Wed Dec 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.2-1
- Update to 2.2.2 & Fix CVE-2024-34069
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.1-3
- Update release to compile with python 3.10
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
