%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name i18n

Name: rubygem-i18n
Version:        1.6.0
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
Summary:        Support for ruby.
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/i18n/versions/%{version}
Source0:        https://rubygems.org/downloads/i18n-%{version}.gem
%define sha1    i18n=8975d7778f14387d6dc555886156956e6309d578
BuildRequires:  ruby >= 1.9.3
Requires:       rubygem-concurrent-ruby > 1.0

%description
New wave Internationalization support for Ruby.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Feb 09 2022 Harinadh <hdommaraju@vmware.com> 1.6.0-1
-   Version update
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.1.0-1
-   Update to version 1.1.0
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 0.8.6-1
-   Initial build
