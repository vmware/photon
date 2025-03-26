%global debug_package %{nil}
%global gem_name strptime

Name: rubygem-strptime
Version:        0.2.5
Release:        5%{?dist}
Summary:        a fast strptime/strftime engine which uses VM
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/strptime-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby-devel
Requires:       ruby

%description
a fast strptime/strftime engine which uses VM

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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.5-5
-   Release bump for SRP compliance
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.5-4
-   Add gem macros
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.5-3
-   Build from source
*   Fri Nov 25 2022 Shivani Agarwal <shivania2@vmware.com> 0.2.5-2
-   Version bump to build with new ruby
*   Sat Sep 26 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.5-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.4-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.2.3-1
-   Initial build
