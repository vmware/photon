%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name public_suffix

Name: rubygem-public_suffix
Version:        4.0.6
Release:        1%{?dist}
Summary:        PublicSuffix can parse and decompose a domain name into top level domain, domain and subdomains.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    public_suffix=49a74818d2831eeee54499a90f855276c9acd936
BuildRequires:  ruby >= 2.1.0

BuildArch: noarch

%description
PublicSuffix can parse and decompose a domain name into top level domain, domain and subdomains.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.6-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 3.1.1-2
-   Built with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.1.1-1
-   Initial build
