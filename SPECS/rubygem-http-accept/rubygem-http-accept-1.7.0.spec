%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-accept

Name:           rubygem-http-accept
Version:        1.7.0
Release:        2%{?dist}
Summary:        Parse Accept and Accept-Language HTTP headers.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=de263630227768a4cd5c8fa3b84eef54c6273ad207bc6958dd8b27dcee955ba3d6caf2972e9bd07f8aa03235d1ad9f260c1cdb66e83b24d69d0366fde28335b8

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby

Requires: ruby

BuildArch: noarch

%description
Parse Accept and Accept-Language HTTP headers.

%prep
%autosetup -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.0-2
- Release bump for SRP compliance
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.7.0-1
- Initial version.
- Needed by rubygem-fluent-plugin-kubernetes_metadata_filter.
