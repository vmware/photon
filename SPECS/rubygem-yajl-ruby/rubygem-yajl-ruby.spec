%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name yajl-ruby

Name: rubygem-yajl-ruby
Version:        1.4.1
Release:        2%{?dist}
Summary:        Ruby C bindings to the excellent Yajl JSON stream-based parser library.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/yajl-ruby-%{version}.gem
%define sha1    yajl-ruby=04d0aa7b51a015bd9b3383d4d561fd9067981f76
BuildRequires:  ruby
Provides: rubygem-yajl-ruby = %{version}

%description
Ruby C bindings to the excellent Yajl JSON stream-based parser library.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.4.1-2
-   Rebuilt using ruby-2.7.1
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.4.1-1
-   Update to version 1.4.1
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
-   Initial build
