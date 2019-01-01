%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name msgpack

Name: rubygem-msgpack
Version:        1.2.4
Release:        2%{?dist}
Summary:        A binary-based efficient object serialization library
Group:          Development/Languages
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/msgpack-%{version}.gem
%define sha1    msgpack=d5a0a24034e704de7bc9a56c1497ad5e83cf123e
BuildRequires:  ruby
Provides: rubygem-msgpack = %{version}

%description
MessagePack is a binary-based efficient object serialization library.
It enables to exchange structured objects between many languages like JSON.
But unlike JSON, it is very fast and small.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.2.4-2
-   Increment the release version as part of ruby upgrade
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.4-1
-   Initial build
