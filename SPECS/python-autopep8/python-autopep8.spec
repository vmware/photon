%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        autopep8 automatically formats Python code
Name:           python3-autopep8
Version:        1.4.4
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/python-autopep8/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        python-autopep8-%{version}.tar.gz
%define sha1    python-autopep8=3622f89aa0993654411b82168fd251324b07f512

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

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
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.4.4-2
-   Mass removal python2
*   Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> 1.4.4-1
-   Initial packaging for Photon
