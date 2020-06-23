%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name cool.io

Name: rubygem-cool-io
Version:        1.6.0
Release:        1%{?dist}
Summary:        a high performance event framework for Ruby which uses the libev C library
Group:          Development/Languages
License:        N/A
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/cool.io-%{version}.gem
%define sha1    cool.io=7fd26857eba28eb0b71b85c84e7872e21e2d8291
BuildRequires:  ruby
Provides: rubygem-cool-io = %{version}

%description
a high performance event framework for Ruby which uses the libev C library

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.5.3-1
-   Initial build
