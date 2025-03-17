Summary:        A Universal Character Encoding Detector in Python
Name:           python3-chardet
Version:        5.0.0
Release:        2%{?dist}
Url:            https://pypi.org/project/chardet
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/chardet/chardet/archive/chardet-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.0.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 5.0.0-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.0.0-1
- Add python3-setuptools to Requires
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.0.4-2
- Mass removal python2
* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 3.0.4-1
- Initial packaging.
