%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name thread_safe

Name: rubygem-thread_safe
Version:        0.3.6
Release:        1%{?dist}
Summary:        Thread safe programming support for Ruby.
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/activesupport/thread_safe/%{version}
Source0:        https://rubygems.org/downloads/thread_safe-%{version}.gem
%define sha1    thread_safe=5a60162d065d0f479d61ba0a11734b44f5f7ef19
BuildRequires:  ruby

%description
A collection of data structures and utilities to make thread-safe programming in Ruby easier

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 0.3.6-1
-   Initial build
