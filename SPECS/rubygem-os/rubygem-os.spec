%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name os

Summary:        The OS gem allows for some easy telling if you're on windows or not.
Name:           rubygem-os
Version:        1.1.4
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=988eccce8c32aafecdaeec6eb09e079699a2da886e5763541e93f3374d82963cc6582eb905e353008e3ac8a2994eff0e7f9e6bf8005dc10eeb7956cfd949dd48

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

%if 0%{?with_check}
BuildRequires: git
%endif

Requires: ruby

%description
The OS gem allows for some easy telling if you’re on windows or not. OS.windows?
as well as some other helper utilities

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%check
cd %{buildroot}%{gemdir}/gems/%{gem_name}-%{version}
[[ $(ruby -r"./lib/os" -e "puts OS.cpu_count") -gt 0 ]] || exit 1
[[ "$(ruby -r"./lib/os" -e "puts OS.bits")" =~ ^(32|64)$ ]] || exit 1

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.4-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.4-1
- Initial version.
