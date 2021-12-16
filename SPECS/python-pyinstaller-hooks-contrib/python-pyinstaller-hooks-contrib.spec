%define debug_package %{nil}

Summary:        PyInstaller hooks contrib is a required module during pyinstaller installation.
Name:           python3-pyinstaller-hooks-contrib
Version:        2020.9
Release:        2%{?dist}
Url:            https://pypi.org/project/pyinstaller-hooks-contrib
License:        GPLv2+
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://files.pythonhosted.org/packages/ab/65/53a41d4788b8cbdd38c1f3404d07ca11c37e59a36170c10077e6ce001a3f/pyinstaller-hooks-contrib-%{version}.tar.gz
%define sha1    pyinstaller-hooks-contrib=54bf66681fe374627c3b00def35d3137ee022cdc

BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  python3-macros

Requires:       python3

Provides:       python3.9dist(pyinstaller-hooks-contrib)

%description
Pyinstaller contrib hooks consist of  hooks for many packages, and allows PyInstaller to work with these packages seamlessly.

%prep
%autosetup -p1 -n pyinstaller-hooks-contrib-%{version}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2020.9-2
- Add Provides pyinstaller-hooks-contrib
* Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 2020.9-1
- Initial packaging for Photon.
