%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name io-event

Name:           rubygem-io-event
Version:        1.1.0
Release:        1%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=b95e0a9c7e38e4116af1cdd3a00d3f5c59b676e11393789f3859d8b03310ccb177c0d240f00e6a0c184548f9316322a416ad4a4960da645e1c787d96b0495a11

BuildRequires:  ruby

Requires: ruby

BuildArch: noarch

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
* Fri Dec 15 2023 Shivani Agrawal <shivania2@vmware.com> 1.1.0-1
- Initial version. Needed by fiber-local.
