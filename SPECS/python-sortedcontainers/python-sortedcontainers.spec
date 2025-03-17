Summary:        Pure Python sorted container types
Name:           python3-sortedcontainers
Version:        2.4.0
Release:        2%{?dist}
URL:            http://www.python.org
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/e8/c4/ba2f8066cceb6f23394729afe52f3bf7adec04bf9ed2c820b39e19299111/sortedcontainers-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides:       python%{python3_version}dist(sortedcontainers) = %{version}-%{release}

%description
SortedContainers is an Apache2 licensed sorted collections library, written in \
pure-Python, and fast as C-extensions.

%prep
%autosetup -p1 -n sortedcontainers-%{version}

%build
%py3_build

%install
%py3_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{python3_sitelib}/sortedcontainers*.egg-info/*
%{python3_sitelib}/sortedcontainers/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.4.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.4.0-1
- Automatic Version Bump
* Sat Sep 19 2020 Susant Sahani <ssahaniv@vmware.com> 2.2.2-1
- Initial rpm release.
