%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-docopt
Version:        0.6.2
Release:        2%{?dist}
Summary:        Pythonic argument parser to create command line interfaces.
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/docopt
Source0:        docopt-%{version}.tar.gz
%define sha1    docopt=224a3ec08b56445a1bd1583aad06b00692671e04
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools

BuildArch:      noarch

%description
docopt helps easily create most beautiful command-line interfaces.

%prep
%setup -n docopt-%{version}

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
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 0.6.2-2
-   Mass removal python2
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.6.2-1
-   Initial version of python-docopt package for Photon.
