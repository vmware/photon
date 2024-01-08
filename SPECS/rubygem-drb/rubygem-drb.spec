%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name drb

Name:           rubygem-drb
Version:        2.2.0
Release:        1%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=3397710719b35dd591d48298b992949903e8d3f721a9a10ac6edef44cae4fd857e4fb538b149a89a53877a043729aaf2426cd4c0cbad4a3d788ac687798573b2

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
* Thu Jan 4 2024 Shivani Agrawal <shivania2@vmware.com> 2.2.0-1
- Initial version. Needed by activesupport
