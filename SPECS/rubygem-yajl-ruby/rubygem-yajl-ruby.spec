%global debug_package %{nil}
%global gem_name yajl-ruby

Name: rubygem-yajl-ruby
Version:        1.4.1
Release:        4%{?dist}
Summary:        Ruby C bindings to the excellent Yajl JSON stream-based parser library.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/yajl-ruby-%{version}.gem
%define sha512  yajl-ruby=24cd82380658d784bbf0a7a16d4048125cc5a856b0e0b4d3bdec29a550a9131d3959f9a75eba0d18d5db8d0a23158fb7ef6ea6f60d221a7bc3d8efc437d52df5

BuildRequires:  ruby-devel

Requires:       ruby

%description
Ruby C bindings to the excellent Yajl JSON stream-based parser library.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.1-4
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.1-3
-   Build from source
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.4.1-2
-   Rebuilt using ruby-2.7.1
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.4.1-1
-   Update to version 1.4.1
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
-   Initial build
