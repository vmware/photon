Summary:        A Universal Character Encoding Detector in Python
Name:           python3-chardet
Version:        4.0.0
Release:        1%{?dist}
Url:            https://pypi.org/project/chardet
License:        LGPL v2.1
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/chardet/chardet/archive/chardet-%{version}.tar.gz
%define sha512 chardet=ebd7f420e1094445270db993f6373ffe7370419e002b0bb13299dc6c9b0f7c4e77b0f44f871fba6371e6869e7c86728514367db377e3137487a3acf50cb81e96

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-setuptools

BuildArch:      noarch

%description
chardet is a universal character encoding detector in Python.

%prep
%autosetup -p1 -n chardet-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
%pytest -v
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/chardetect

%changelog
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.0.0-1
- Add python3-setuptools to Requires
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.0.4-2
- Mass removal python2
* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 3.0.4-1
- Initial packaging.
