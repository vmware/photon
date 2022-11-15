Name:           python3-geomet
Version:        0.1.2
Release:        1%{?dist}
Summary:        GeoJSON <-> WKT/WKB conversion utilities
License:        Apache Software License
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
URL:            https://pypi.python.org/packages/source/s/geomet/geomet-%{version}.tar.gz

Source0: geomet-%{version}.tar.gz
%define sha512 geomet=f66706a8a412b195ecb1601bb1e4e9e366b3f390d97dd1cc8eb5161ed8b3e649f4d10044b2cf68bb18ad11d3ac6bc971cd32c080d29ac5443741e716a9ceb670

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-six
Requires:       python3-click
Requires:       python3-setuptools

BuildArch:      noarch

%description
Convert GeoJSON to WKT/WKB (Well-Known Text/Binary), and vice versa.

%prep
%autosetup -p1 -n geomet-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/geomet
%{python3_sitelib}/*

%changelog
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 0.1.2-1
- Initial packaging for Photon
