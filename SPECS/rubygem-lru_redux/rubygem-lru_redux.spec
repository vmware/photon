%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name lru_redux

Name:           rubygem-lru_redux
Version:        1.1.0
Release:        4%{?dist}
Summary:        An efficient, thread safe implementation of an LRU cache.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  lru_redux=b489ec89fbe4e2ab06f967a1c21ca487026151a93ebf782538fd0626657d39b0a7ed45ff4c24388b2c45d9cdcb622ae8c56eade5c5da27e2c31f110ad5bc8c2c

BuildRequires:  ruby >= 1.9.3
BuildRequires:  findutils

Requires:       ruby

BuildArch:      noarch

%description
An efficient, thread safe implementation of an LRU cache.

%prep
gem unpack %{SOURCE0}
%autosetup -p1 -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
gem install %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}%{gemdir}/cache
mkdir -p %{buildroot}%{gemdir}/doc
mkdir -p %{buildroot}%{gemdir}/plugins
mkdir -p %{buildroot}%{gemdir}/specifications
mkdir -p %{buildroot}%{gemdir}/gems
mkdir -p %{buildroot}%{gemdir}/extensions
cp -pa %{gemdir}/build_info %{buildroot}%{gemdir}/
cp -pa %{gemdir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gemdir}/cache/
cp -pa %{gemdir}/doc/%{gem_name}-%{version} %{buildroot}%{gemdir}/doc/
cp -pa %{gemdir}/plugins %{buildroot}%{gemdir}/
cp -pa %{gemdir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gemdir}/specifications
cp -pa %{gemdir}/gems/%{gem_name}-%{version} %{buildroot}%{gemdir}/gems
[ -d %{buildroot}%{_libdir} ] && find %{buildroot}%{_libdir} -type f -perm /022 -exec chmod go-w {} \;

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Feb 28 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-4
-   Bump version with ruby upgrade
*   Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.0-3
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.1.0-2
-   Rebuilt using ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.0-1
-   Initial build
