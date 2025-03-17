%global debug_package %{nil}
%global gem_name lru_redux

Name:           rubygem-lru_redux
Version:        1.1.0
Release:        6%{?dist}
Summary:        An efficient, thread safe implementation of an LRU cache.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel
BuildRequires:  findutils

BuildArch:      noarch

%description
An efficient, thread safe implementation of an LRU cache.

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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-6
-   Release bump for SRP compliance
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-5
-   Add gem macros
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-4
-   Build from source
*   Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.0-3
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.1.0-2
-   Rebuilt using ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.0-1
-   Initial build
