%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A tool to check your Python code
Name:           python3-pycodestyle
Version:        2.5.0
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/python-pam/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        python-pycodestyle-%{version}.tar.gz
%define sha1    python-pycodestyle=8d25df191e57d6602bc8ccaf6f6d4f84181301d6

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
%description
pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.


%prep
%setup -q -n pycodestyle-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/pycodestyle

%changelog
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.5.0-2
-   Mass removal python2
*   Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> 2.5.0-1
-   Initial packaging for Photon
