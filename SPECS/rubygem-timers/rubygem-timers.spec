%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name timers

Name: rubygem-timers
Version:        4.3.5
Release:        3%{?dist}
Summary:        Schedule procs to run after a certain time, or at periodic intervals, using any API that accepts a timeout.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=075b9c530b62e91ec4de995d1fc88667aac71372ef455343059294f075d57d6bcd52a36e182bd6b735852c9bfd8f0319d676ae377aaf060b857f5f3060b9e7c2

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel

Requires: ruby

BuildArch: noarch

%description
Schedule procs to run after a certain time, or at periodic intervals, using any API that accepts a timeout.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.3.5-3
-   Build gems properly
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.3.5-2
-   Bump Version to build with new ruby
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 4.3.5-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 4.3.2-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 4.3.0-2
-   Rebuilt using ruby-2.7.1
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 4.3.0-1
-   Initial build
