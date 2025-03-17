Summary:        Module to simplify usage of decorators
Name:           python3-decorator
Version:        5.1.1
Release:        2%{?dist}
Group:          Development/Languages/Python
URL:            https://pypi.org/project/decorator
Source0:        decorator-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
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
%autosetup -n decorator-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root)
%doc CHANGES.md
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
*   Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.1.1-2
-   Release bump for SRP compliance
*   Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 5.1.1-1
-   Automatic Version Bump
*   Thu Mar 19 2020 Tapas Kundu <tkundu@vmware.com> 4.4.2-1
-   Initial release.
