Summary:        The PyPA recommended tool for installing Python packages.
Name:           python3-pip
Version:        23.0.1
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pip/
Source0:        https://files.pythonhosted.org/packages/6b/8b/0b16094553ecc680e43ded8f920c3873b01b1da79a54274c98f08cb29fca/pip-%{version}.tar.gz
%define sha512 pip=f85523d44ccf81b340cc63964441e7ce4c9c0296518ec8fee742692c05b470b02263be810d2f4806bc9fc10d4fcfbeb75bfb3f1cc4509a54955804a4fbb21e1e
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
* Tue Feb 07 2023 Prashant S Chauhan <psinghchauha@vmware.com> 23.0.1-1
- Separate python3-pip from python3 spec.
