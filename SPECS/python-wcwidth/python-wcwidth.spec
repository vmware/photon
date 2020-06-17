%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Measures number of Terminal column cells of wide-character codes.
Name:           python3-wcwidth
Version:        0.1.7
Release:        3%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/wcwidth
Source0:        https://files.pythonhosted.org/packages/source/w/wcwidth/wcwidth-%{version}.tar.gz
%define         sha1 wcwidth=28df2f5e8cd67ec182d822350252fea9bc3a91c8

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
This Library is mainly for those implementing a Terminal Emulator, or programs that carefully produce output to be interpreted by one.

%prep
%setup -q -n wcwidth-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.1.7-3
-   Mass removal python2
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.7-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.7-1
-   Initial packaging for Photon
