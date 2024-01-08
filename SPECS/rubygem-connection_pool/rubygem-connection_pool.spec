%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name connection_pool

Name:           rubygem-connection_pool
Version:        2.2.5
Release:        1%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=3bc4e4d241cd4b1adb00d341aafe7795bbf0eff459ace962670d83c20c0eaa0d42f49a1f5e61c2327ff4fcbf3abfbc6f6c910f7a31d4a0f62bc55c782ab20e45

BuildRequires:  ruby

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
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 2.2.5-1
- Initial version. Needed by rubygem-activesupport.
