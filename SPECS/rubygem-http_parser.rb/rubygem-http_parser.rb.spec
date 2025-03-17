%global debug_package %{nil}
%global gem_name http_parser.rb

Name: rubygem-http_parser.rb
Version:        0.8.0
Release:        4%{?dist}
Summary:        Provides ruby bindings to http parser
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/http_parser.rb-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby-devel

%description
Provides ruby bindings to http parser.

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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.8.0-4
-   Release bump for SRP compliance
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.8.0-3
-   Add gem macros
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.8.0-2
-   Update build command, to build with source code
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.8.0-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.6.0-2
-   rebuilt with ruby-2.7.1
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.6.0-1
-   Initial build
