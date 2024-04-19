%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name netrc

Name: rubygem-netrc
Version:        0.11.0
Release:        3%{?dist}
Summary:        This library can read and update netrc files, preserving formatting including comments and whitespace.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  netrc=7f0df3f79d92b891d40a49e9b893ca7131077195cf15453b155e37e68e29f8cd3810ba791a06338058262c8cb8fed56c87c295e450c133b428b3398eb99e683a
BuildRequires:  ruby

BuildArch: noarch

%description
This library can read and update netrc files, preserving formatting including comments and whitespace.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.11.0-3
- Bump Version to build with new ruby
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.11.0-2
-   Rebuilt using ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.11.0-1
-   Initial build
