%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name yajl-ruby
%global ruby_ver 3.1.0

Name:           rubygem-yajl-ruby
Version:        1.4.3
Release:        2%{?dist}
Summary:        Ruby C bindings to the excellent Yajl JSON stream-based parser library.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/yajl-ruby-%{version}.gem
%define sha512  yajl-ruby=8cfde677f11ad80a468dce7876b97aa87fa35d78fcd727d4542e00c09cc28d1cca3301cf7c4e1f773edf2192262ec8d6ffab93b11d488d2b048d8013f6c7645a

BuildRequires:  ruby

Requires:       ruby

Provides:       rubygem-yajl-ruby = %{version}

%description
Ruby C bindings to the excellent Yajl JSON stream-based parser library.

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
* Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.3-2
- Build from source
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.4.3-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.4.1-2
- Rebuilt using ruby-2.7.1
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.4.1-1
- Update to version 1.4.1
* Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
- Initial build
