Summary:        WebOb provides objects for HTTP requests and responses..
Name:           python3-webob
Version:        1.8.6
Release:        3%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/WebOb
Source0:        https://pypi.python.org/packages/1a/2b/322d6e01ba19c1e28349efe46dab1bd480c81a55af0658d63dc48ed62ee6/WebOb-%{version}.tar.gz
%define sha512  WebOb=b9a3faac114c55f3e9a6eb71a78dd921d928da99a427dea05bc798bc1fe249f0f1cf8c9b9fcb1b73be2737b9132bbfe2250a8652e3a8a1199ac74fa62a59d44c

Patch0:         CVE-2024-42353.patch

BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description
WebOb provides objects for HTTP requests and responses. Specifically it does this by wrapping the WSGI request environment and response status/headers/app_iter(body).

The request and response objects provide many conveniences for parsing HTTP request and forming HTTP responses. Both objects are read/write: as a result, WebOb is also a nice way to create HTTP requests and parse HTTP responses.

%prep
%autosetup -p1 -n WebOb-%{version}
%{__rm} -f tests/performance_test.py

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Dec 23 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.8.6-3
- Fix CVE-2024-42353
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.8.6-2
- Bump up to compile with python 3.10
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.6-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 1.8.2-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.8.2-1
- Update to version 1.8.2
* Mon Aug 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.2-3
- Fixed make check errors
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.2-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Mar 30 2017 Siju Maliakkal <smaliakkal@vmware.com> 1.7.2-1
- Updating package to 1.7.2-1
* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.1-1
- Initial packaging for Photon
