%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rest-client

Name: rubygem-rest-client
Version:        2.1.0
Release:        4%{?dist}
Summary:        A simple HTTP and REST client for Ruby, inspired by the Sinatra microframework style of specifying actions: get, put, post, delete.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  rest-client=fe5d44409dfe607566b4c0324441d9a3981776699027bfbc92283b1cd425f204211fc872593cb0784e0ca7a5e061e98793540eedfeb1891d9a8afd53a5ce01de

BuildRequires: ruby-devel
BuildRequires: rubygem-http-accept
BuildRequires: rubygem-http-cookie
BuildRequires: rubygem-mime-types
BuildRequires: rubygem-netrc

Requires: rubygem-http-accept >= 1.7.0, rubygem-http-accept < 2.0.0
Requires: rubygem-http-cookie >= 1.0.2, rubygem-http-cookie < 2.0.0
Requires: rubygem-mime-types >= 1.16.0, rubygem-mime-types < 4.0.0
Requires: rubygem-netrc >= 0.8.0, rubygem-netrc < 1.0.0
Requires: ruby

BuildArch: noarch

%description
A simple HTTP and REST client for Ruby, inspired by the Sinatra microframework style of specifying actions: get, put, post, delete.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
mkdir -p %{buildroot}%{_bindir}
%gem_install
ln -srv %{buildroot}%{gemdir}/bin/restclient %{buildroot}/%{_bindir}/restclient

%files
%defattr(-,root,root,-)
%{gemdir}
%{_bindir}/restclient

%changelog
*   Tue Mar 04 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1.0-4
-   Build gems properly
*   Mon Jan 08 2024 Shivani Agarwal <shivania2@vmware.com> 2.1.0-3
-   Fix requires
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 2.1.0-2
-   rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.1.0-1
-   Initial build
