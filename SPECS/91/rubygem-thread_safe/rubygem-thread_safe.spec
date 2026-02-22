%global build_if %{photon_subrelease} <= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name thread_safe

Name: rubygem-thread_safe
Version:        0.3.6
Release:        5.1%{?dist}
Summary:        Thread safe programming support for Ruby.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/activesupport/thread_safe/%{version}
Source0:        https://rubygems.org/downloads/thread_safe-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
A collection of data structures and utilities to make thread-safe programming in Ruby easier

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Feb 13 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.3.6-5.1
- Bump after moving to SPECS/91
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.3.6-5
- Spec bump with ruby upgrade
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.3.6-4
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.3.6-3
- Release bump for SRP compliance
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.3.6-2
- Rebuilt using ruby-2.7.1
* Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 0.3.6-1
- Initial build
