%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name concurrent-ruby

Name: rubygem-concurrent-ruby
Version:        1.0.5
Release:        2%{?dist}
Summary:        Modern concurrency tools for Rails framework.
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/concurrent-ruby/versions/%{version}
Source0:        https://rubygems.org/downloads/concurrent-ruby-%{version}.gem
%define sha1    concurrent-ruby=87de0558473d73a2f7fb208c9b462cd5a894a7c6
BuildRequires:  ruby

%description
Modern concurrency tools including agents, futures, promises, thread pools, actors,
supervisors, and more. Inspired by Erlang, Clojure, Go, JavaScript, actors, and
classic concurrency patterns.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.0.5-2
-   Increment the release version as part of ruby upgrade
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.5-1
-   Initial build
