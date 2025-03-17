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
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/dig_rb-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.0.1-3
-   Release bump for SRP compliance
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.1-2
-   Rebuilt using ruby-2.7.1
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
-   Initial build
