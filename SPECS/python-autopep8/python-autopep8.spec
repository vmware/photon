%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        autopep8 automatically formats Python code
Name:           python3-autopep8
Version:        1.5.4
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/python-autopep8/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        autopep8-%{version}.tar.gz
%define sha1    autopep8=9260df6f3d29b5faeb67ec8d789fe85e5f6fca54

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-toml

Requires:       python3-toml
Requires:       python3
Requires:       python3-libs

%description
autopep8 automatically formats Python code to conform to the PEP 8 style guide.
It uses the pycodestyle utility to determine what parts of the code needs to be
formatted.


%prep
%setup -q -n autopep8-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/autopep8

%changelog
*   Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.5.4-2
-   Add python3-toml to requires
*   Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.4-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.3-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.4.4-2
-   Mass removal python2
*   Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> 1.4.4-1
-   Initial packaging for Photon
