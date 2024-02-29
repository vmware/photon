%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mini_portile2

Summary:        Simplistic port-like solution for developers
Name:           rubygem-mini_portile2
Version:        2.8.5
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}
Source0:        https://rubygems.org/downloads/mini_portile2-%{version}.gem
%define sha512  mini_portile2=fa09bc2c4aefc341cb249dc33b5ad3182aa582ef150645793e323bdef4d19cbeeced0348c3c962a7225a9aa91b40824347fa1499955326525eddcf867f6ff798

BuildRequires:  ruby

Requires:       ruby

%description
Simplistic port-like solution for developers. It provides a standard and simplified way to compile against dependency libraries without messing up your system.

%prep
%autosetup -c -T
%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.8.5-1
-   Update to version 2.8.5
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.8.0-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.0-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.3.0-1
-   Update to version 2.3.0
*   Wed Mar 22 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.0-1
-   Updated to version 2.1.0
*   Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 2.0.0-3
-   Bump up release number to reflect ruby upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.0-2
-   GA - Bump release of all rpms
*   Mon Mar 07 2016 Xiaolin Li <xiaolinl@vmware.com>
-   Initial build
