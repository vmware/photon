%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A Universal Character Encoding Detector in Python
Name:           python-chardet
Version:        3.0.4
Release:        1%{?dist}
URL:            https://pypi.org/project/chardet/
License:        LGPL v2.1
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/chardet/chardet/archive/chardet-%{version}.tar.gz
%define sha1    chardet=bf740348e002581b026dc4af47d56479097c1fcd

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:	python-pytest
BuildRequires:	python3-pytest
%endif

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
chardet is a universal character encoding detector in Python.

%package -n     python3-chardet
Summary:        python3-chardet


Requires:       python3
Requires:       python3-libs

%description -n python3-chardet
Python 3 version of chardet.

%prep
%setup -q -n chardet-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
# TODO

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-chardet
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/chardetect

%changelog
*   Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 3.0.4-1
-   Initial packaging.
