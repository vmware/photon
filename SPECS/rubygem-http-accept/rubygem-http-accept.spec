%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-accept

Name: rubygem-http-accept
Version:        1.7.0
Release:        3%{?dist}
Summary:        Parse Accept and Accept-Language HTTP headers.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    http-accept=0f8c31dacdd69d0398844101af792103dc600e1f
BuildRequires:  ruby

BuildArch: noarch

%description
Parse Accept and Accept-Language HTTP headers.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-3
-   Downgrade to 1.7.0 for rubygem-rest-client 2.1.0
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.7.0-2
-   rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.7.0-1
-   Initial build
