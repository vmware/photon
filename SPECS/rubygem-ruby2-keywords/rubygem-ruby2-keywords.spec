%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ruby2_keywords

Name:           rubygem-ruby2-keywords
Version:        0.0.5
Release:        1%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=f6b9078b111e68c0017e0025ecdccb976c7a32f35c1a8adf9fd879db0c91f89eb9bd799f9527a846e28056f2a5fbf0f3610cda9538570288c493613c35c83a6f

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
* Thu Jan 04 2024 Shivani Agrawal <shivania2@vmware.com> 0.0.5-1
- Initial version. Needed by activesupport.
