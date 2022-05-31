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
%define sha512  yajl-ruby=24cd82380658d784bbf0a7a16d4048125cc5a856b0e0b4d3bdec29a550a9131d3959f9a75eba0d18d5db8d0a23158fb7ef6ea6f60d221a7bc3d8efc437d52df5
Patch0:         CVE-2022-24795.patch
BuildRequires:  ruby
Provides: rubygem-yajl-ruby = %{version}

%description
Ruby C bindings to the excellent Yajl JSON stream-based parser library.

%prep
%autosetup -n yajl-ruby-%{version} -p1

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue May 31 2022 Tapas Kundu <tkundu@vmware.com> 1.4.1-2
-   Fix CVE-2022-24795
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.4.1-1
-   Update to version 1.4.1
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
-   Initial build
