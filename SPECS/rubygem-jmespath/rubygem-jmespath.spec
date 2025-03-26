%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name jmespath

Name: rubygem-jmespath
Version:        1.6.1
Release:        2%{?dist}
Summary:        Implements JMESPath for Ruby.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/jmespath-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby

%description
Implements JMESPath for Ruby.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.6.1-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.4.0-2
-   rebuilt with ruby-2.7.1
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
-   Initial build
