Summary:        The PyPA recommended tool for installing Python packages.
Name:           python3-pip
Version:        23.3.2
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pip/
Source0:        https://files.pythonhosted.org/packages/6b/8b/0b16094553ecc680e43ded8f920c3873b01b1da79a54274c98f08cb29fca/pip-%{version}.tar.gz
%define sha512 pip=b2d8bcff02fe196163e88e02702861bfccba202e5c71d8c6843eeebc84066efa6987574e26a89ff25f096645e99c824dde585fbae415b66d5eb88657bb4d9cb4
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-xml
BuildArch:      noarch

%description
pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes.

%prep
%autosetup -p1 -n pip-%{version}

%build
%{py3_build}

%install
%{py3_install}
find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f

%check
%{py3_test}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 755)
%{python3_sitelib}/*
%{_bindir}/pip*

%changelog
* Wed Jan 24 2024 Prashant S Chauhan <psinghchauha@vmware.com> 23.3.2-1
- Update to 23.3.2
* Tue Feb 07 2023 Prashant S Chauhan <psinghchauha@vmware.com> 23.0.1-1
- Separate python3-pip from python3 spec.
