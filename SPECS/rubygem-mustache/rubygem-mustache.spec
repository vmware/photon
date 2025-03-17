%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mustache

Name: rubygem-mustache
Version:        1.1.1
Release:        3%{?dist}
Summary:        A framework-agnostic way to render logic-free views
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ruby >= 2.0

%description
Mustache is a replacement for your views. Instead of views consisting of
ERB or HAML with random helpers and arbitrary logic, your views are broken
into two parts: a Ruby class and an HTML template

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.1-3
-   Release bump for SRP compliance
*   Thu Dec 08 2022 Shivani Agarwal <shivania2@vmware.com> 1.1.1-2
-   Bump version to build with new Ruby
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.1.1-1
-   Initial build
