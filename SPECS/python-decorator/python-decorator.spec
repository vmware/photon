%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Module to simplify usage of decorators
Name:           python3-decorator
Version:        4.4.2
Release:        1%{?dist}
License:        BSD License (new BSD License)
Group:          Development/Languages/Python
URL:            https://pypi.org/project/decorator
Source0:        decorator-%{version}.tar.gz
%define         sha1 decorator=24d4560ff3e89a6cec068d323383577343c086fb
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-xml
Requires:       python3

%description
The goal of the decorator module is to make it easy to define signature-preserving function decorators and decorator
factories. It also includes an implementation of multiple dispatch and other niceties (please check the docs).

%prep
%setup -q -n decorator-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%doc CHANGES.md
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
*   Thu Mar 19 2020 Tapas Kundu <tkundu@vmware.com> 4.4.2-1
-   Initial release.
