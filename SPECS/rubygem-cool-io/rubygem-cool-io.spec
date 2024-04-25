%global debug_package %{nil}
%global gem_name cool.io

Name:           rubygem-cool-io
Version:        1.8.0
Release:        2%{?dist}
Summary:        a high performance event framework for Ruby which uses the libev C library
Group:          Development/Languages
License:        N/A
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/cool.io-%{version}.gem
%define sha512  cool.io=e847bafbc157d05f1d48b262856a68d80b183a9eed29d6d454df4fbe7fabc427e6e83c873a0f36f2f8cc06bebac22cc1993f344943e43faaf556a8b235666026
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
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.8.0-2
-   Add gem macros
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.8.0-1
-   Update to version 1.8.0
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
