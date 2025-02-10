%define srcname             pip
%define python_wheel_dir    %{_datadir}/python-wheels
%define python_wheel_name   %{srcname}-%{version}-py3-none-any.whl

Summary:        The PyPA recommended tool for installing Python packages.
Name:           python3-pip
# if you make any security fix in this package, package the whl files
# python3.spec without miss
Version:        23.3.2
Release:        3%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pip/

Source0: https://files.pythonhosted.org/packages/6b/8b/0b16094553ecc680e43ded8f920c3873b01b1da79a54274c98f08cb29fca/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=b2d8bcff02fe196163e88e02702861bfccba202e5c71d8c6843eeebc84066efa6987574e26a89ff25f096645e99c824dde585fbae415b66d5eb88657bb4d9cb4

Patch0: dummy-certifi.patch
Patch1: fix-for-requests-CVE-2024-35195.patch
Patch2: fix-for-requests-CVE-2024-35195-2.patch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-wheel
BuildRequires:  ca-certificates

Requires:       python3
Requires:       python3-setuptools
Requires:       python3-xml
Requires:       %{name}-wheel = %{version}-%{release}

BuildArch:      noarch

%description
Pip is the package installer for Python.
You can use pip to install packages from the Python Package Index and
other indexes.

%package        wheel
Summary:        The pip wheel
Requires:       ca-certificates

%description wheel
A Python wheel of pip to use with venv.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{python3} setup.py bdist_wheel

%install
%{python3} dist/%{python_wheel_name}/pip install \
    --root %{buildroot} \
    --no-deps \
    --disable-pip-version-check \
    --progress-bar off \
    --verbose \
    --ignore-installed \
    --no-warn-script-location \
    --no-index \
    --no-cache-dir \
    --find-links dist \
    'pip==%{version}'

find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -vf

mkdir -p %{buildroot}%{python_wheel_dir}
install -p dist/%{python_wheel_name} -t %{buildroot}%{python_wheel_dir}

%check
%{py3_test}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,755)
%{python3_sitelib}/*
%{_bindir}/pip*

%files wheel
%defattr(-,root,root,755)
%dir %{python_wheel_dir}
%{python_wheel_dir}/%{python_wheel_name}

%changelog
* Mon Feb 10 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 23.3.2-3
- Fix CVE-2024-35195 in _vendors/requests
* Tue Feb 20 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 23.3.2-2
- Add wheel files
* Wed Jan 24 2024 Prashant S Chauhan <psinghchauha@vmware.com> 23.3.2-1
- Update to 23.3.2
* Tue Feb 07 2023 Prashant S Chauhan <psinghchauha@vmware.com> 23.0.1-1
- Separate python3-pip from python3 spec.
