%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sigv4

Name: rubygem-aws-sigv4
Version:        1.5.2
Release:        2%{?dist}
Summary:        Amazon Web Services Signature Version 4 signing library.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sigv4-%{version}.gem
%define sha512    aws-sigv4=7a756e3faafaa31046b1a17a825e8e1b88899914435cd1d7811089105f4d31020d24b81c1e8e86efa9a7446a768399323389e14462f1117a9f74f0dbbe2fbc62

Source1: license.txt
%include %{SOURCE1}
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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.5.2-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.5.2-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.2-1
-   Automatic Version Bump
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.3-1
-   Initial build
