%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-hpack

Name: rubygem-protocol-hpack
Version:        1.4.1
Release:        1%{?dist}
Summary:        A compresssor and decompressor for HTTP 2.0 HPACK.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    protocol-hpack=06f6a9e2fa1d38dec5724ced2bcc55f0c4eeb1c4
BuildRequires:  ruby

BuildArch: noarch

%description
Provides a compressor and decompressor for HTTP 2.0 headers, HPACK, as defined by RFC7541.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.4.1-1
-   Initial build
