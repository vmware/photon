%global debug_package %{nil}
%global gem_name cool.io

Name: rubygem-cool-io
Version:        1.7.0
Release:        3%{?dist}
Summary:        a high performance event framework for Ruby which uses the libev C library
Group:          Development/Languages
License:        N/A
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/cool.io-%{version}.gem
%define sha512  cool.io=e443fdd71a6bd0dd8409b7285a4fcea880aae2a43fc5687f664caa936ff4304b522bc07e148bdd51c91f8847ed2f482c5bbcee435dfab5282cf1114a47686d95

BuildRequires:  ruby-devel
Requires:       ruby

%description
a high performance event framework for Ruby which uses the libev C library

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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.0-3
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.0-2
-   Build from source
*   Sat Sep 26 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
-   Automatic Version Bump
*   Thu Sep 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.5.3-1
-   Initial build
