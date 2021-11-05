%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name lru_redux

Name:           rubygem-lru_redux
Version:        1.1.0
Release:        2%{?dist}
Summary:        An efficient, thread safe implementation of an LRU cache.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    lru_redux=7767aae39ca4e93beed18979845c490685655790
BuildRequires:  ruby >= 1.9.3
BuildRequires:  findutils
BuildArch:      noarch

%description
An efficient, thread safe implementation of an LRU cache.

%prep
%autosetup -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
[ -d %{buildroot}/usr/lib ] && find %{buildroot}/usr/lib -type f -perm /022 -exec chmod go-w {} \;

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.0-2
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.0-1
-   Initial build
