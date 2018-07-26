%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name yajl-ruby

Name: rubygem-yajl-ruby
Version:        1.4.0
Release:        1%{?dist}
Summary:        Ruby C bindings to the excellent Yajl JSON stream-based parser library.
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/yajl-ruby-%{version}.gem
%define sha1    yajl-ruby=c58802fb3f351963e7f89b8f0d55f871a70a2b97
BuildRequires:  ruby
Provides: rubygem-yajl-ruby = %{version}

%description
Ruby C bindings to the excellent Yajl JSON stream-based parser library.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
-   Initial build
