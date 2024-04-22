%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name unf_ext
%global ruby_ver 3.3.0

Name: rubygem-unf_ext
Version:        0.0.9.1
Release:        1%{?dist}
Summary:        Unicode Normalization Form support library for CRuby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  unf_ext=f2d0d58dc0ed30e3e99ac75022c8ea78bf4ad51c8803009c059de087b1cd439e06a8e7ef4c1be5c75048f85afe6c301f402ed21405ff02ad36ea73209416994d
BuildRequires:  ruby
BuildRequires:  gmp-devel
Requires:       ruby

%description
Unicode Normalization Form support library for CRuby.

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
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.0.9.1-1
-   Update to version 0.0.9.1
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.0.8.2-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.0.7.7-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-2
-   Enabled build for non x86_64 build archs
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-1
-   Initial build
