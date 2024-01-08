%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-pool

Name:           rubygem-async-pool
Version:        0.2.0
Release:        1%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=08dcb0776b505d369eb16549f63f93252aa91d1627261039f9e7f231574436914c3e036e02393bc8070c1c0296e76f2c9a5823884a5aead3bc6ffb6f3f52ae19

BuildRequires:  ruby

Requires: ruby
Requires: rubygem-async

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
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 0.2.0-1
- Initial version. Needed by rubygem-async-http.
