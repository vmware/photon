Summary:        Module to simplify usage of decorators
Name:           python3-decorator
Version:        5.1.1
Release:        1%{?dist}
License:        BSD License (new BSD License)
Group:          Development/Languages/Python
URL:            https://pypi.org/project/decorator
Source0:        decorator-%{version}.tar.gz
%define sha512  decorator=584857ffb0c3e52344b473ceb9e28adfd7d789d480a528471f8ab37be055ebe5feb170f41077010e25350e1c311189d45b90773cf12f0043de98ea8ebcde20ab
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
*   Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 5.1.1-1
-   Automatic Version Bump
*   Thu Mar 19 2020 Tapas Kundu <tkundu@vmware.com> 4.4.2-1
-   Initial release.
