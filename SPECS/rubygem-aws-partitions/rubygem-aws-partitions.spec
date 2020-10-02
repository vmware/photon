%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-partitions

Name: rubygem-aws-partitions
Version:        1.379.0
Release:        1%{?dist}
Summary:        Provides interfaces to enumerate AWS partitions, regions & services.
Group:          Development/Languages
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-partitions-%{version}.gem
%define sha1    aws-partitions=5f4bd18720c22bfe0efccf6a2bf417d894bb704e
BuildRequires:  ruby

%description
Provides interfaces to enumerate AWS partitions, regions, and services.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
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
