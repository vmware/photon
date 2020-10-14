%define debug_package %{nil}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        PyInstaller hooks contrib is a required module during pyinstaller installation.
Name:           python3-pyinstaller-hooks-contrib
Version:        2020.9
Release:        1%{?dist}
Url:            https://pypi.org/project/pyinstaller-hooks-contrib
License:        GPLv2+
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/ab/65/53a41d4788b8cbdd38c1f3404d07ca11c37e59a36170c10077e6ce001a3f/pyinstaller-hooks-contrib-%{version}.tar.gz
%define sha1    pyinstaller-hooks-contrib=54bf66681fe374627c3b00def35d3137ee022cdc
BuildRequires:  python3
BuildRequires:  python3-setuptools
Requires:       python3

%description
Pyinstaller contrib hooks consist of  hooks for many packages, and allows PyInstaller to work with these packages seamlessly.

%prep
%setup -q -n pyinstaller-hooks-contrib-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root=%{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Wed Oct 14 2020 Piyush Gupta <gpiyush@vmware.com> 2020.9-1
-   Initial packaging for Photon.
