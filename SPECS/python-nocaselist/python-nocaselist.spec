Name:           python3-nocaselist
Version:        1.0.4
Release:        2%{?dist}
Summary:        A case-insensitive list for Python
License:        Apache Software License (Apache Software License 2.0)
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/fe/5c/bfb5a421027852e577491ebfa6f9e454066bd430b4b7007692776c45da62/nocaselist-1.0.4.tar.gz
Source0:        nocaselist-%{version}.tar.gz
%define sha1    nocaselist=9ceadbaedbbb10dc0c644a6ec5a438dc93d27ac6
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch
Provides:       python%{python3_version }dist(nocaselist)

%description
A case-insensitive list for Python

%prep
%autosetup -n nocaselist-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.4-2
-   Update release to compile with python 3.10
*   Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.0.4-1
-   Initial packaging for python3-nocaselist
