%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name serverengine

Name: rubygem-serverengine
Version:        2.0.7
Release:        1%{?dist}
Summary:        A framework to implement robust multiprocess servers like Unicorn
Group:          Development/Languages
License:        Apache 2
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/serverengine-%{version}.gem
%define sha1    serverengine=e3901a234a7e4ae66428536621af71e273c8af8a
BuildRequires:  ruby > 2.1.0
Provides: rubygem-serverengine = %{version}

%description
A framework to implement robust multiprocess servers like Unicorn.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 2.0.7-1
-   Initial build
