%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pure Python Vi Implementation.
Name:           python-pyvim
Version:        2.0.22
Release:        2%{?dist}
License:        UNKNOWN
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/service_identity
Source0:        pyvim-%{version}.tar.gz
%define sha1    pyvim=b44c9e78755b1f13ee45a2903758386425e9a2ba
# To get tests:
# git clone https://github.com/jonathanslenders/pyvim.git && cd pyvim
# git checkout 6860c413 && tar -czvf ../pyvim-tests-0.0.20.tar.gz tests/
Source1:        pyvim-tests-%{version}.tar.gz
%define sha1 pyvim-tests=57c48d48d1e20ae997975a99504be26191b2a662

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python-pytest
BuildRequires:  python-prompt_toolkit
BuildRequires:  python3-pytest
BuildRequires:  python3-prompt_toolkit
%endif

Requires:       python2
Requires:       python2-libs
Requires:       python-prompt_toolkit

BuildArch:      noarch

%description
An implementation of Vim in Python.

%package -n     python3-pyvim
Summary:        python-pyvim

Requires:       python3
Requires:       python3-libs
Requires:       python3-prompt_toolkit
%description -n python3-pyvim
Python 3 version.

%prep
%setup -q -n pyvim-%{version}
tar -xf %{SOURCE1} --no-same-owner

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
*   Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 2.0.22-2
-   Use --no-same-owner for tar
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.0.22-1
-   Update to version 2.0.22
*   Mon Jul 24 2017 Divya Thaluru <dthaluru@vmware.com> 0.0.20-4
-   Fixed runtime dependencies and make check errors
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.20-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.0.20-2
-   Rectified python3 version
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.0.20-1
-   Initial packaging for Photon.
