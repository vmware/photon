Summary:        Fast, reliable, and secure dependency management.
Name:           yarn
Version:        1.21.1
Release:        1%{?dist}
License:        BSD 2-Clause
URL:            https://yarnpkg.com
Source0:        https://github.com/yarnpkg/yarn/archive/%{name}-%{version}.tar.gz
%define sha1    yarn=88bcbdfb28c27c8348f92b327826111cba116c11
Source1:        node_modules_yarn_1.21.tar.gz
%define sha1    node_modules_yarn=0017116df1538cde49ef06635811343b167c3d92
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Developement/Languages/NodeJs
Patch0:         CVE-2020-8131-Fix-arbitrary-file-write-on-fetch.patch
BuildRequires:  nodejs = 8.17.0

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
*   Tue Jun 09 2020 Tapas Kundu <tkundu@vmware.com> 1.21.1-1
-   Update to 1.21.1
*   Thu Apr 02 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.10.1-8
-   Add patch to fix CVE-2019-15608
*   Thu Mar 05 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.10.1-7
-   Add patch to fix CVE-2020-8131
*   Wed Feb 12 2020 Siju Maliakkal <smaliakkal@vmware.com> 1.10.1-6
-   To use nodejs 8.17.0
*   Tue Jan 07 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.10.1-5
-   Add patch to fix CVE-2019-10773
*   Wed Oct 09 2019 Tapas Kundu <tkundu@vmware.com> 1.10.1-4
-   Use local repo for installing yarn
*   Thu Sep 12 2019 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.10.1-3
-   Add patch to fix CVE-2019-5448
*   Thu Apr 25 2019 Ankit Jain <ankitja@vmware.com> 1.10.1-2
*   Added version to the nodejs
*   Mon Feb 11 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.10.1-1
-   Upgrade to 1.10.1 for buildrequirement of kibana
*   Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
-   Initial yarn package for PhotonOS.
