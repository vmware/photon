%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python PAM module using ctypes, py3/py2
Name:           python3-pam
Version:        1.8.4
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/python-pam/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        python-pam-%{version}.tar.gz
%define sha1    python-pam=5c3074a85c6cd510de2f996a908390a1ed70bd9f

BuildArch:      noarch
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description
Python PAM module using ctypes, py3/py2.

%prep
%setup -q -n python-pam-%{version}

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
*   Thu Feb 18 2021 Tapas Kundu <tkundu@vmware.com> 1.8.4-1
-   Initial packaging for Photon
