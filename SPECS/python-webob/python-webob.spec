Summary:        WebOb provides objects for HTTP requests and responses..
Name:           python3-webob
Version:        1.8.7
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/WebOb
Source0:        https://pypi.python.org/packages/1a/2b/322d6e01ba19c1e28349efe46dab1bd480c81a55af0658d63dc48ed62ee6/WebOb-%{version}.tar.gz
%define sha512  WebOb=ff6a1ce796a59d9c078dc908a0d6307a080230a5c806be2278eebcbb78016bed43067e78e3e4a6d72a5f51184c137e8267ac75cbb92b057db008b51a792ff489

BuildArch:      noarch

%if %{with_check}
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
%autosetup -n WebOb-%{version}
%{__rm} -f tests/performance_test.py

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.8.7-1
- Automatic Version Bump
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
