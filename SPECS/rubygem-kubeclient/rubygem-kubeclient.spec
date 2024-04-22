%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name kubeclient

Name:           rubygem-kubeclient
Version:        4.11.0
Release:        1%{?dist}
Summary:        A client for Kubernetes REST api.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=f32a9df1a0d56a2b128eb2377191ab61548d3873561eeaf46d6cb271d5b5ba29ca7a9df2dac6ff130c357e41ab2cfe6e307140c9255d2962f5ff5eb89c6ae144

BuildRequires:  ruby
BuildRequires:  findutils

Requires: rubygem-activesupport
Requires: rubygem-http >= 3.0, rubygem-http < 5.1.1
Requires: rubygem-recursive-open-struct > 1.1
Requires: rubygem-rest-client
Requires: rubygem-http >= 3.0, rubygem-http < 5.0
Requires: rubygem-http-accept >= 1.7.0, rubygem-http-accept < 2.0
Requires: rubygem-jsonpath
Requires: ruby

BuildArch: noarch

%description
A client for Kubernetes REST api.

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
[ -d %{buildroot}%{_libdir} ] && find %{buildroot}%{_libdir} -type f -perm /022 -exec chmod go-w {} \;

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.11.0-1
-   Update to version 4.11.0
* Sat Oct 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.10.1-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 4.10.1-1
- Automatic Version Bump
* Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 4.9.1-2
- Drop group write permissions for files in /usr/lib to comply with STIG
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 4.9.1-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.1.4-2
- Rebuilt with ruby-2.7.1
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.4-1
- Initial build
