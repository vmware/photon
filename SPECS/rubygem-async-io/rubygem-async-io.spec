%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-io

Name:           rubygem-async-io
Version:        1.41.0
Release:        1%{?dist}
Summary:        Provides support for asynchonous TCP, UDP, UNIX and SSL sockets.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=e067053c052117da8ab799bb7b3e2c8ed61bb1d0635d7b4ac13e582aa3d0e716b4ea3053e8391b1558cdb0e062bc2f7fbf71d9072caeebc6cacd77cf25977964

BuildRequires:  ruby >= 2.3.0, ruby < 3.3.1

Requires: rubygem-async >= 1.14.0, rubygem-async < 2.8.3
Requires: rubygem-fiber-local
Requires: ruby
Requires: rubygem-fiber-annotation

BuildArch: noarch

%description
Async::IO provides builds on async and provides asynchronous wrappers for IO, Socket, and related classes.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.41.0-1
-   Update to version 1.41.0
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.34.0-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.34.0-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.30.1-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.30.0-1
- Automatic Version Bump
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.25.0-1
- Initial build
