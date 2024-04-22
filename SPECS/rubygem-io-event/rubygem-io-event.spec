%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name io-event
%global ruby_ver 3.1.0

Name:           rubygem-io-event
Version:        1.1.0
Release:        2%{?dist}
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
gem unpack %{SOURCE0}
cd %{gem_name}-%{version}
/bin/chmod -Rf a+rX,u+w,g-w,o-w .
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
cd %{gem_name}-%{version}
gem build %{gem_name}.gemspec
gem install %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gemdir}/{cache,doc,plugins,specifications,gems,extensions/%{_arch}-linux/%{ruby_ver}}
cp -a %{gemdir}/build_info %{buildroot}%{gemdir}/
cp -a %{gemdir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gemdir}/cache/
cp -a %{gemdir}/doc/%{gem_name}-%{version} %{buildroot}%{gemdir}/doc/
cp -a %{gemdir}/plugins %{buildroot}%{gemdir}/
cp -a %{gemdir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gemdir}/specifications/
cp -a %{gemdir}/gems/%{gem_name}-%{version} %{buildroot}%{gemdir}/gems/
cp -a %{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}/%{gem_name}-%{version} %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-2
- Build from source
* Fri Dec 15 2023 Shivani Agrawal <shivania2@vmware.com> 1.1.0-1
- Initial version. Needed by fiber-local.
