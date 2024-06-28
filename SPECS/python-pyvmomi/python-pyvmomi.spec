Summary:        pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.
Name:           python3-pyvmomi
Version:        7.0.3
Release:        1%{?dist}
License:        OSI Approved :: Apache Software License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/pyvmomi
Source0:        pyvmomi-%{version}.tar.gz
%define sha512  pyvmomi=b4229e95cc0747136374d2c95a393d05fca1af7335c58ef946edf27c7114b366844a5994b7644c04439b30eb9103bfc5c1d6db0ad68ef0798cbcc945893c4fa4
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
%endif
Requires:       python3
BuildArch:      noarch

%description
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.

%prep
%autosetup -p1 -n pyvmomi-%{version}

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
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 7.0.3-1
- Automatic Version Bump
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 7.0.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 7.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 6.7.0.2018.9-3
- Mass removal python2
* Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 6.7.0.2018.9-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 6.7.0.2018.9-1
- Update to version 6.7.0.2018.9
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 6.5-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 6.5-1
- Initial packaging for Photon.
