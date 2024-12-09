%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-partitions

Name: rubygem-aws-partitions
Version:        1.654.0
Release:        2%{?dist}
Summary:        Provides interfaces to enumerate AWS partitions, regions & services.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-partitions-%{version}.gem
%define sha512    aws-partitions=8c6b38c5facfb7dc4c915daba3f160f21e277998aa4887edbc20037b20ca356cd9133057407833c34a08cb76495ea61dd61fb7c24e9e43a8f1626a98cf1c59d3

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby

%description
Provides interfaces to enumerate AWS partitions, regions, and services.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.654.0-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.654.0-1
-   Automatic Version Bump
*   Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.379.0-1
-   Automatic Version Bump
*   Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.378.0-1
-   Automatic Version Bump
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.377.0-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.375.0-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.363.0-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.104.0-1
-   Update to version 1.104.0
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.96.0-1
-   Initial build
