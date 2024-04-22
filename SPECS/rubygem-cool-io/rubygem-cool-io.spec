%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name cool.io
%global ruby_ver 3.3.0

Name:           rubygem-cool-io
Version:        1.8.0
Release:        1%{?dist}
Summary:        a high performance event framework for Ruby which uses the libev C library
Group:          Development/Languages
License:        N/A
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/cool.io-%{version}.gem
%define sha512  cool.io=e847bafbc157d05f1d48b262856a68d80b183a9eed29d6d454df4fbe7fabc427e6e83c873a0f36f2f8cc06bebac22cc1993f344943e43faaf556a8b235666026
BuildRequires:  ruby >= 3.1.2
Requires:       ruby >= 3.1.2
Provides: rubygem-cool-io = %{version}

%description
a high performance event framework for Ruby which uses the libev C library

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
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.8.0-1
-   Update to version 1.8.0
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.7.1-1
-   Automatic Version Bump
*   Sat Sep 26 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
-   Automatic Version Bump
*   Thu Sep 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.5.3-1
-   Initial build
