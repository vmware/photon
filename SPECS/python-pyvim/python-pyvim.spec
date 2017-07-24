%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pure Python Vi Implementation.
Name:           python-pyvim
Version:        0.0.20
Release:        4%{?dist}
License:        UNKNOWN
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/service_identity
Source0:        pyvim-%{version}.tar.gz
%define         sha1 pyvim-%{version}=0bcda6d5f01be0b334f8bdf974b23c3f65e023ae
# To get tests:
# git clone https://github.com/jonathanslenders/pyvim.git && cd pyvim
# git checkout 6860c413 && tar -czvf ../pyvim-tests-0.0.20.tar.gz tests/
Source1:        pyvim-tests-%{version}.tar.gz
%define sha1 pyvim-tests=480cec56514ea5ff0387e72c53bbddb951d95954

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  python-pytest
BuildRequires:  python-prompt_toolkit
%endif

Requires:       python2
Requires:       python2-libs
Requires:       python-prompt_toolkit

BuildArch:      noarch

%description
An implementation of Vim in Python.

%package -n     python3-pyvim
Summary:        python-pyvim
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-prompt_toolkit
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-prompt_toolkit
%description -n python3-pyvim
Python 3 version.

%prep
%setup -q -n pyvim-%{version}
tar -xf %{SOURCE1}

%build
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/pyvim %{buildroot}/%{_bindir}/pyvim3
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
PYTHONPATH=./ py.test2
PYTHONPATH=./ py.test3

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/pyvim

%files -n python3-pyvim
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/pyvim3

%changelog
*   Mon Jul 24 2017 Divya Thaluru <dthaluru@vmware.com> 0.0.20-4
-   Fixed runtime dependencies and make check errors
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.20-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.0.20-2
-   Rectified python3 version
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.20-1
-   Initial packaging for Photon.
