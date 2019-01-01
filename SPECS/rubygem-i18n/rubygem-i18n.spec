%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name i18n

Name: rubygem-i18n
Version:        0.8.6
Release:        2%{?dist}
Summary:        Support for ruby.
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/i18n/versions/%{version}
Source0:        https://rubygems.org/downloads/i18n-%{version}.gem
%define sha1    i18n=f68d29046b21296ecbb1117d7933bcbbc5edd84c
BuildRequires:  ruby

%description
New wave Internationalization support for Ruby.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 0.8.6-2
-   Increment the release version as part of ruby up
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 0.8.6-1
-   Initial build
