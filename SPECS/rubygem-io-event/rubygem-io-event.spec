%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name io-event

Name:           rubygem-io-event
Version:        0.4.0
Release:        1%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=4db7f3b64bdb06aed0502d4802cedfb407f19221222f13ab137bf2b85c814578cbe87bb9ec3cfada10b1140d5ce2f21544ad260f73354cc6fc4fefada10e59f7

BuildRequires:  ruby

Requires: ruby

%description
Provides low level cross-platform primitives for constructing
event loops, with support for select, kqueue, epoll and io_uring.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Dec 15 2023 Shivani Agrawal <shivania2@vmware.com> 0.4.0-1
- Initial version. Needed by fiber-local.
