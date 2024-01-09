Summary:        autopep8 automatically formats Python code
Name:           python3-autopep8
Version:        1.5.4
Release:        4%{?dist}
Url:            https://pypi.python.org/pypi/python-autopep8/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        autopep8-%{version}.tar.gz
%define sha512 autopep8=e613295d080149028361715f748fc9db1b7fc6212ca4e117594a10c3924a67eaad6ff8d94cfcf2c3dea087e0aa1ce6bcadc1b4eb3f07915daa5b002a09913f59

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-toml

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-tools
BuildRequires: python3-pycodestyle
%endif

Requires:       python3-toml
Requires:       python3
Requires:       python3-libs
Requires:       python3-pycodestyle
Requires:       python3-tools

%description
autopep8 automatically formats Python code to conform to the PEP 8 style guide.
It uses the pycodestyle utility to determine what parts of the code needs to be
formatted.

%prep
%autosetup -p1 -n autopep8-%{version}

%build
%{py3_build}

%install
%{py3_install}

%if 0%{?with_check}
%check
%pytest -v
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/autopep8

%changelog
* Tue Jan 09 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.5.4-4
- Add python3-tools and python3-pycodestyle in Requires
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.4-3
- Bump up to compile with python 3.10
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.5.4-2
- Add python3-toml to requires
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.4-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.3-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.4.4-2
- Mass removal python2
* Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> 1.4.4-1
- Initial packaging for Photon
