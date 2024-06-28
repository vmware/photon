%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http2

Name:           rubygem-protocol-http2
Version:        0.14.2
Release:        2%{?dist}
Summary:        A low level implementation of the HTTP/2 protocol.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=4ab78fdf626939a1e95b2c231da50f449ab53889204cd5bfbf0316b8ed28eb0c8046c5805c23962594abe0959d5f743ee60efd42e093ff822eaf81e74f62bb10

BuildRequires:  ruby

Requires: rubygem-protocol-hpack >= 1.4.0, rubygem-protocol-hpack < 2.0.0
Requires: rubygem-protocol-http >= 0.2.0, rubygem-protocol-http < 1.0.0
Requires: rubygem-async-io
Requires: rubygem-io-event
Requires: ruby

BuildArch: noarch

%description
Provides a low-level implementation of the HTTP/2 protocol.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Sun Oct 22 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.14.2-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.14.2-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.14.1-1
- Automatic Version Bump
* Wed Sep 2 2020 Sujay G <gsujay@vmware.com> 0.9.5-2
- Rebuilt with ruby-2.7.1
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.9.5-1
- Initial build
