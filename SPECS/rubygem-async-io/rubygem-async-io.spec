%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-io

Name: rubygem-async-io
Version:        1.30.1
Release:        2%{?dist}
Summary:        Provides support for asynchonous TCP, UDP, UNIX and SSL sockets.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  async-io=804abe8da97040c1cfd890028f7c57bec3ea6500d5b1e05c444071b8b0291e8063a976293345cb378df6c2a8a25f7d06b0a0453b83c84162fdd5fa40c5ecc221

BuildRequires:  ruby >= 2.3.0, ruby < 3.0.0

Requires: rubygem-async >= 1.14.0, rubygem-async < 2.0.0
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
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.30.1-2
-   Fix requires
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.30.1-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.30.0-1
-   Automatic Version Bump
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.25.0-1
-   Initial build
