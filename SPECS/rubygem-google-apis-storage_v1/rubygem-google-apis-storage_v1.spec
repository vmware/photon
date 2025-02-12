%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-apis-storage_v1

Summary:        This is a simple REST client for Cloud Storage JSON API V1
Name:           rubygem-google-apis-storage_v1
Version:        0.49.0
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=9892d06fe4f6f652c4bf95a5885ee975fbdc4565f52ef635ab3dc43cf24a03ecba3fad8811a7c77f5783a54d09c26e0b8938476567ac8b9bdcdaa8cf3a79351f

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-retriable
BuildRequires: rubygem-addressable
BuildRequires: rubygem-googleauth
BuildRequires: rubygem-httpclient
BuildRequires: rubygem-google-apis-core

Requires: ruby
Requires: rubygem-retriable
Requires: rubygem-addressable
Requires: rubygem-googleauth
Requires: rubygem-httpclient
Requires: rubygem-google-apis-core

%description
This is the simple REST client for Cloud Storage JSON API V1.
Simple REST clients are Ruby client libraries that provide access to Google services
via their HTTP REST API endpoints. These libraries are generated and updated
automatically based on the discovery documents published by the service, and they
handle most concerns such as authentication, pagination, retry, timeouts, and logging.
You can use this client to access the Cloud Storage JSON API, but note that some services
may provide a separate modern client that is easier to use.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.49.0-1
- Initial version.
