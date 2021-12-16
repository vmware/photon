Summary:        A port of the caching algorithms in httplib2 for use with requests session object.
Name:           python3-CacheControl
Version:        0.12.6
Release:        2%{?dist}
License:        Apache Software License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/ionrock/cachecontrol/archive/v%{version}.tar.gz

Source0:        CacheControl-%{version}.tar.gz
%define sha1    CacheControl=213bd9dd49b9a4b8ea6aa797cd86f4ce19ed13a7

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3-requests
Requires:       python3-msgpack

BuildArch:      noarch

%description
CacheControl is a port of the caching algorithms in httplib2 for use with requests session object.
It was written because httplib2's better support for caching is often mitigated by its lack of threadsafety.
The same is true of requests in terms of caching.

%prep
%autosetup -p1 -n CacheControl-%{version}

%build
%py3_build

%install
%py3_install
mv %{buildroot}%{_bindir}/doesitcache %{buildroot}%{_bindir}/doesitcache3

%check
%if 0%{?with_check:1}
python3 setup.py test
%endif

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/doesitcache3

%changelog
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.12.6-2
- Bump up to compile with python 3.10
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.12.6-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 0.12.5-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.12.5-1
- Update to version 0.12.5
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.12.3-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu May 25 2017 Xiaolin Li <xiaolinl@vmware.com> 0.12.3-1
- Initial version
