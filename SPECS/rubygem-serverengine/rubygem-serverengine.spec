%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name serverengine

Name: rubygem-serverengine
Version:        2.2.1
Release:        1%{?dist}
Summary:        A framework to implement robust multiprocess servers like Unicorn
Group:          Development/Languages
License:        Apache 2
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/serverengine-%{version}.gem
%define sha1    serverengine=d6f704b8ce4d05c029a548f28783086828c8fc84
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
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.1-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 2.0.7-1
-   Initial build
