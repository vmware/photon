Summary:        Fast, reliable, and secure dependency management.
Name:           yarn
Version:        1.10.1
Release:        1%{?dist}
License:        BSD 2-Clause
URL:            https://yarnpkg.com
Source0:        https://github.com/yarnpkg/yarn/archive/%{name}-%{version}.tar.gz
%define sha1    yarn=2f5d4c9e3fe876108d3e48db6645332195676e95
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Developement/Languages/NodeJs
BuildArch:      noarch
BuildRequires:  nodejs = 8.11.4

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
npm prune --production

%install
mkdir -p %{buildroot}%{_datadir}/%{name}/bin
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}/lib
mkdir -p %{buildroot}%{_datadir}/%{name}/node_modules
cp -pr bin/ lib/ node_modules/ %{buildroot}%{_datadir}/%{name}/
cp package.json %{buildroot}%{_datadir}/%{name}/package.json
ln -sf %{_datadir}/%{name}/bin/yarn %{buildroot}%{_bindir}/yarn
ln -sf %{_datadir}/%{name}/bin/yarnpkg %{buildroot}%{_bindir}/yarnpkg

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/yarn
%{_bindir}/yarnpkg
%{_datadir}/%{name}/bin/*
%{_datadir}/%{name}/package.json
%{_datadir}/%{name}/lib/*
%{_datadir}/%{name}/node_modules/*
%exclude %{_datadir}/%{name}/node_modules/.bin/*
%exclude %{_datadir}/%{name}/bin/yarn.ps1

%changelog
*   Thu Sep 19 2019 Siju Maliakkal <ssmaliakkal@vmware.com> 1.10.1-1
-   Upgrade to 1.10.1 buildrequirement of kibana, Merged from 3.0
*   Wed Oct 24 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
-   Initial yarn package for PhotonOS.
