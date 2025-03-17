%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-hpack

Name: rubygem-protocol-hpack
Version:        1.4.2
Release:        2%{?dist}
Summary:        A compresssor and decompressor for HTTP 2.0 HPACK.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby

BuildArch: noarch

%description
Provides a compressor and decompressor for HTTP 2.0 headers, HPACK, as defined by RFC7541.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.2-2
-   Release bump for SRP compliance
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.2-1
-   Automatic Version Bump
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.4.1-1
-   Initial build
