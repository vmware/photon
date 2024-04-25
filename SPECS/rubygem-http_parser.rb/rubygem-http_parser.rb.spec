%global debug_package %{nil}
%global gem_name http_parser.rb

Name: rubygem-http_parser.rb
Version:        0.6.0
Release:        4%{?dist}
Summary:        Provides ruby bindings to http parser
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/http_parser.rb-%{version}.gem
%define sha512  http_parser.rb=51c29bfc85de8cedb4e98fec84c955252556abaa4d0848fbc38b232879ffc946c72acf38440e8e9f1e31a8b734a68d43a96924af5f48ac4f1a054153ec913a08
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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.6.0-4
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.6.0-3
-   Update build command, to build with source code
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.6.0-2
-   rebuilt with ruby-2.7.1
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.6.0-1
-   Initial build
