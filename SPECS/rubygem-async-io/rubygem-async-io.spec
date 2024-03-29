%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-io

Name:           rubygem-async-io
Version:        1.34.0
Release:        2%{?dist}
Summary:        Provides support for asynchonous TCP, UDP, UNIX and SSL sockets.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=513bf5f97e2653ee46395c3f67d3a092ed94dedfb74183cde2479d9fb7cd21ff1ca22939ff4e406ef7845ad301c14e251b61c6ec3cc27c81b7dd9bb387115276

BuildRequires:  ruby >= 2.3.0, ruby < 3.1.3

Requires: rubygem-async >= 1.14.0, rubygem-async < 2.2.2
Requires: rubygem-fiber-local
Requires: ruby

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
