%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name tzinfo

Name: rubygem-tzinfo
Version:        2.0.5
Release:        2%{?dist}
Summary:        Timezone related support for Ruby.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/tzinfo/versions/%{version}
Source0:        https://rubygems.org/downloads/tzinfo-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby

%description
TZInfo provides daylight savings aware transformations between times in different time zones.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/tzinfo-%{version}
gem install thread_safe
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.0.5-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.5-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
-   Automatic Version Bump
*   Tue Nov 27 2018 Sujay G <gsujay@vmware.com> 1.2.5-2
-   Added %check section
*   Tue Aug 14 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.5-1
-   Upgraded to 1.2.5
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.2.3-1
-   Initial build
