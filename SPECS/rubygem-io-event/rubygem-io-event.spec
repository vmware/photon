%global debug_package %{nil}
%global gem_name io-event

Name:           rubygem-io-event
Version:        1.1.0
Release:        5%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel

Requires: ruby

%description
Provides low level cross-platform primitives for constructing
event loops, with support for select, kqueue, epoll and io_uring.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-5
- Release bump for SRP compliance
* Wed Sep 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.0-4
- Remove noarch
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-3
- Add gem macros
* Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-2
- Build from source
* Fri Dec 15 2023 Shivani Agrawal <shivania2@vmware.com> 1.1.0-1
- Initial version. Needed by fiber-local.
