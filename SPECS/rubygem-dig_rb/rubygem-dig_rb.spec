%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name dig_rb

Name: rubygem-dig_rb
Version:        1.0.1
Release:        3%{?dist}
Summary:        Array/Hash/Struct#dig backfill for ruby
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/dig_rb-%{version}.gem
%define sha512  dig_rb=2c27271b41ffa1a884b2fc836d91efd93eeb9ceead49fd500bb62027f8f17160c2cca76fcabcc6fd3361c353ba4f0b3ddbefbe0a7016732d4e3e57b76c679382
BuildRequires:  ruby
Provides: rubygem-dig_rb = %{version}

%description
Array/Hash/Struct#dig backfill for ruby

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.1-3
-   Bump Version to build with new ruby
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.1-2
-   Rebuilt using ruby-2.7.1
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
-   Initial build
