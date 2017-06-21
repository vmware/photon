%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pure Python Vi Implementation.
Name:           python-pyvim
Version:        0.0.20
Release:        3%{?dist}
License:        UNKNOWN
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/service_identity
Source0:        pyvim-%{version}.tar.gz
%define         sha1 pyvim=0bcda6d5f01be0b334f8bdf974b23c3f65e023ae

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
An implementation of Vim in Python.

%package -n     python3-pyvim
Summary:        python-pyvim
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs
%description -n python3-pyvim
Python 3 version.

%prep
%setup -q -n pyvim-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/pyvim %{buildroot}/%{_bindir}/pyvim3
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/pyvim

%files -n python3-pyvim
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/pyvim3

%changelog
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.20-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.0.20-2
-   Rectified python3 version
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.20-1
-   Initial packaging for Photon.
