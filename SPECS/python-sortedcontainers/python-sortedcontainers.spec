Summary:        Pure Python sorted container types
Name:           python3-sortedcontainers
Version:        2.2.2
Release:        1%{?dist}
License:        ASL 2.0
URL:            http://www.python.org
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/grantjenks/python-sortedcontainers/archive/v%{version}/python-sortedcontainers-%{version}.tar.gz
%define sha512 python-sortedcontainers=4a7da8d76111b56bda432b211c11ef48ac8af25ddf7fd961cf72628c18f878a6c2a22e272e108f3e5ad88a333b8f646b54c8dd11c9c642349c9da001140abd16

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides:       python3.9dist(sortedcontainers) = %{version}-%{release}

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
* Sat Sep 19 2020 Susant Sahani <ssahaniv@vmware.com> 2.2.2-1
- Initial rpm release.
