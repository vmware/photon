%global debug_package %{nil}
%global gem_name io-event

Name:           rubygem-io-event
Version:        1.4.4
Release:        2%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=8a11aecb9019a2154110b900e99fe19325daa554d15a60261093b56edae9c23ceec4d54616cd11be4a5dede5e73c4bba144d40621e80ad2203a3d2261f06d178

BuildRequires:  ruby-devel

Requires: ruby

BuildArch: noarch

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
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.4-2
- Add gem macros
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.4-1
- Update to version 1.4.4
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-1
- Initial version. Needed by fiber-local.
