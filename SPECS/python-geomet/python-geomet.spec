%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-geomet
Version:        0.1.2
Release:        1%{?dist}
Summary:        GeoJSON <-> WKT/WKB conversion utilities
License:        Apache Software License
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/s/geomet/geomet-%{version}.tar.gz
Source0:        geomet-%{version}.tar.gz
%define sha1    geomet=3b89e10c60ac9abee726dc696a1117d5427d5517

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-six
Requires:       python3-click
Requires:       python3-setuptools

BuildArch:      noarch

%description
Convert GeoJSON to WKT/WKB (Well-Known Text/Binary), and vice versa.

%prep
%setup -n geomet-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{_bindir}/geomet
%{python3_sitelib}/*

%changelog
*   Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 0.1.2-1
-   Initial packaging for Photon
