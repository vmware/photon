%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sigv4

Name:           rubygem-aws-sigv4
Version:        1.8.0
Release:        1%{?dist}
Summary:        Amazon Web Services Signature Version 4 signing library.
Group:          Development/Languages
License:        Apache 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/aws-sigv4-%{version}.gem
%define sha512 %{gem_name}=dc4898a201f81b25f913b37bf0b302066fa9b5e4bb64e317957aa0c34090814585e371c67e1d5776d7b5ef72be25992e2224fcb4e3a1f3e3762dc1fdb54134f8

BuildRequires: ruby

Requires: ruby
Requires: rubygem-aws-eventstream

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
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.8.0-1
-   Update to version 1.8.0
* Thu Oct 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.5.2-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.5.2-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.2-1
- Automatic Version Bump
* Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.3-1
- Initial build
