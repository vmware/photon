%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sigv4

Name: rubygem-aws-sigv4
Version:        1.11.0
Release:        1%{?dist}
Summary:        Amazon Web Services Signature Version 4 signing library.
Group:          Development/Languages
License:        Apache 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sigv4-%{version}.gem
%define sha512  aws-sigv4=2ad243cedbf386c141caa63ccc9c4896a9777946f4330db851ca986c66115464cb6ccba3a20528e719d9c2bb1c386d4095915af9f06209ca1fc565e701ed6dbc
BuildRequires:  ruby

%description
Amazon Web Services Signature Version 4 signing library.
Generates sigv4 signature for HTTP requests.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jan 05 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.11.0-1
-   Bump version to 1.11.0 to be compatible with rubygem-aws-sdk-s3 upgrade
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.2-1
-   Automatic Version Bump
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.3-1
-   Initial build
