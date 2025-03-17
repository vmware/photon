%global debug_package %{nil}
%global gem_name hpricot

Name: rubygem-hpricot
Version:        0.8.6
Release:        5%{?dist}
Summary:        a swift, liberal HTML parser with a fantastic library
Group:          Development/Library
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ruby-devel

%description
Hpricot is a fast, flexible HTML parser written in C. It's designed to be
very accommodating and to have a very helpful library

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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.8.6-5
-   Release bump for SRP compliance
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.8.6-4
-   Add gem macros
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.8.6-3
-   Update build command, to build with source code
*   Fri Nov 25 2022 Shivani Agarwal <shivania2@vmware.com> 0.8.6-2
-   Version bump to build with new ruby
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.6-1
-   Initial build
