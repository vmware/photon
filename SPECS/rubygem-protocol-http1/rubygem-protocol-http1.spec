%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http1

Name:           rubygem-protocol-http1
Version:        0.14.6
Release:        2%{?dist}
Summary:        A low level implementation of the HTTP/1 protocol.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=e9a47a559576e90b3770bac421e043e37c3697f447d2d3d8ee1531be19d8ddc2203f59bfc7baf212fe10cb90656cbdc6470e1061125ab64dd74e84484885ec48

BuildRequires: ruby

Requires: rubygem-protocol-http >= 0.5.0, rubygem-protocol-http < 1.0.0
Requires: rubygem-async-io
Requires: rubygem-io-event
Requires: ruby

BuildArch: noarch

%description
Provides a low-level implementation of the HTTP/1 protocol.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Sun Oct 22 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.14.6-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.14.6-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.13.1-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.9.0-2
- Rebuilt with ruby-2.7.1
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.9.0-1
- Initial build
