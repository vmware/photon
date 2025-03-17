%global debug_package %{nil}
%global gem_name cool.io

Name:           rubygem-cool-io
Version:        1.7.1
Release:        4%{?dist}
Summary:        a high performance event framework for Ruby which uses the libev C library
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/cool.io-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby-devel
Requires:       ruby >= 3.1.2

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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.1-4
-   Release bump for SRP compliance
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.1-3
-   Add gem macros
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.1-2
-   Build from source
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.7.1-1
-   Automatic Version Bump
*   Sat Sep 26 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
-   Automatic Version Bump
*   Thu Sep 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.5.3-1
-   Initial build
