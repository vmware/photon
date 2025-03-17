%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name tzinfo-data

Name: rubygem-tzinfo-data
Version:        1.2022.6
Release:        2%{?dist}
Summary:        data from the IANA Time Zone database packaged as Ruby modules
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/tzinfo-data-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby
Provides: rubygem-tzinfo-data = %{version}

%description
TZInfo::Data contains data from the IANA Time Zone database packaged as
Ruby modules for use with TZInfo.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2022.6-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2022.6-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2020.1-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2018.5-1
-   Initial build
