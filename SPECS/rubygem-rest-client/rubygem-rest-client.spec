%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rest-client

Name: rubygem-rest-client
Version:        2.1.0
Release:        2%{?dist}
Summary:        A simple HTTP and REST client for Ruby, inspired by the Sinatra microframework style of specifying actions: get, put, post, delete.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    rest-client=169e6f1d6a55ae58e066ec37ec899eef14fde9a4
BuildRequires:  ruby >= 2.0.0

Requires: rubygem-http-accept >= 1.7.0, rubygem-http-accept < 2.0.0
Requires: rubygem-http-cookie >= 1.0.2, rubygem-http-cookie < 2.0.0
Requires: rubygem-mime-types >= 1.16.0, rubygem-mime-types < 4.0.0
Requires: rubygem-netrc >= 0.8.0, rubygem-netrc < 1.0.0
BuildArch: noarch

%description
A simple HTTP and REST client for Ruby, inspired by the Sinatra microframework style of specifying actions: get, put, post, delete.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 2.1.0-2
-   rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.1.0-1
-   Initial build
