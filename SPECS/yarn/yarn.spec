Summary:        Fast, reliable, and secure dependency management.
Name:           yarn
Version:        1.10.1
Release:        6%{?dist}
License:        BSD 2-Clause
URL:            https://yarnpkg.com
Source0:        https://github.com/yarnpkg/yarn/archive/%{name}-%{version}.tar.gz
%define sha1    yarn=2f5d4c9e3fe876108d3e48db6645332195676e95
Source1:        node_modules_yarn_1.10.1.tar.gz
%define sha1    node_modules_yarn=81e9e4db4d99783baac50c0dd2aa410a8e465db7
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Developement/Languages/NodeJs
Patch0:         CVE-2019-5448-forces-using-https-for-registries.patch
Patch1:         CVE-2019-10773.patch
Patch2:         CVE-2020-8131-Fix-arbitrary-file-write-on-fetch.patch
Patch3:         CVE-2019-15608.patch
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

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

tar xf %{SOURCE1} --no-same-owner

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
*   Thu Apr 02 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.10.1-6
-   Add patch to fix CVE-2019-15608
*   Thu Mar 05 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.10.1-5
-   Add patch to fix CVE-2020-8131
*   Tue Jan 07 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.10.1-4
-   Add patch to fix CVE-2019-10773
*   Wed Oct 09 2019 Tapas Kundu <tkundu@vmware.com> 1.10.1-3
-   Use local repo for installing yarn
*   Thu Sep 12 2019 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.10.1-2
-   Add patch to fix CVE-2019-5448
*   Wed Feb 13 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.10.1-1
-   Upgrade to 1.10.1 for kibana buildrequirement
*   Mon Jul 09 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
-   Initial yarn package for PhotonOS.
