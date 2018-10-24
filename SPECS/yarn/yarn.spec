Summary:        Fast, reliable, and secure dependency management.
Name:           yarn
Version:        1.6.0
Release:        1%{?dist}
License:        BSD 2-Clause
URL:            https://yarnpkg.com
Source0:        https://github.com/yarnpkg/yarn/archive/%{name}-%{version}.tar.gz
%define sha1    yarn=dca4344aa4aa9b31aebe95636985b6fabc4d0542
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Developement/Languages/NodeJs
BuildRequires:  nodejs

%global debug_package %{nil}

%description
Yarn caches every package it has downloaded, so it never needs to download the same package again. It also does
almost everything concurrently to maximize resource utilization. This means even faster installs.
Using a detailed but concise lockfile format and a deterministic algorithm for install operations, Yarn is able to
guarantee that any installation that works on one system will work exactly the same on another system.
Yarn uses checksums to verify the integrity of every installed package before its code is executed.

%prep
%setup -q -n %{name}-%{version}
npm install

%build
npm run build

%install
mkdir -p %{buildroot}%{_libdir}/node_modules/%{name}
mkdir -p %{buildroot}%{_bindir}
cp -r src bin package.json node_modules lib %{buildroot}%{_libdir}/node_modules/%{name}
ln -sf %{_libdir}/node_modules/%{name}/bin/yarn.js %{buildroot}%{_bindir}/yarn
ln -sf %{_libdir}/node_modules/%{name}/bin/yarn.js %{buildroot}%{_bindir}/yarnpkg

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/yarn
%{_bindir}/yarnpkg
%dir %{_libdir}/node_modules/
%{_libdir}/node_modules/%{name}

%changelog
*   Wed Oct 24 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
-   Initial yarn package for PhotonOS.
