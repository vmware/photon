%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name i18n

Name: rubygem-i18n
Version:        1.8.5
Release:        1%{?dist}
Summary:        Support for ruby.
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/i18n/versions/%{version}
Source0:        https://rubygems.org/downloads/i18n-%{version}.gem
%define sha1    i18n=383b7a07b6111b119d98379195773d9829e9abaf
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
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.5-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.1.0-1
-   Update to version 1.1.0
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 0.8.6-1
-   Initial build
