%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name cool.io

Name: rubygem-cool-io
Version:        1.5.3
Release:        2%{?dist}
Summary:        a high performance event framework for Ruby which uses the libev C library
Group:          Development/Languages
License:        N/A
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/cool.io-%{version}.gem
%define sha1    cool.io=a29fa2b9aafdbb017481906c658d425e47c38264
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
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.5.3-2
-   Increment the release version as part of ruby upgrade
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.5.3-1
-   Initial build
