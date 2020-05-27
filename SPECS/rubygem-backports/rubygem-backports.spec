# Generated from backports-2.5.1.gem by gem2rpm -*- rpm-spec -*-
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name backports

Name: rubygem-backports
Version:        3.11.4
Release:        2%{?dist}
Summary:        Backports of Ruby features for older Ruby
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://github.com/marcandre/backports
Source0:        https://rubygems.org/gems/backports-%{version}.gem
%define sha1    backports=edf08f3a0d9e202048857d78ddda44e59294084c
BuildRequires:  ruby
BuildRequires:  rubygem-activesupport
BuildRequires:  rubygem-i18n
BuildRequires:  rubygem-tzinfo
BuildRequires:  rubygem-thread_safe
BuildRequires:  rubygem-concurrent-ruby
Requires:       rubygem-activesupport
Requires:       rubygem-i18n
Requires:       rubygem-tzinfo
Requires:       rubygem-thread_safe
Requires:       rubygem-concurrent-ruby


%description
Essential backports that enable many of the nice features of Ruby 1.8.7 up to
2.1.0 for earlier versions.

%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/backports-%{version}
# Removal of alias_method_chain method in Rails 5.1 version creates issue
# since the existing testsuite doesn't reflect the change. To avoid rake
# to abort and continue the tests following fix is done.
# ref: https://github.com/marcandre/backports/issues/114
sed -i "s/^/#/" lib/backports/rails/module.rb
rake test

%files
%defattr(-,root,root,-)
%{gemdir}


%changelog
*   Fri Nov 23 2018 Sujay G <gsujay@vmware.com> 3.11.4-2
-   Updated %check section
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 3.11.4-1
-   Update to version 3.11.4
*   Wed Aug 2 2017 Kumar Kaushik <kaushikk@vmware.com> 3.7.0-2
-   Adding requires for test support.
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.0-1
-   Updated to version 3.7.0.
*   Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 3.6.8-3
-   Bump up release number to reflect ruby upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.8-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.6.8-1
-   Upgrade version.
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 3.6.7-1
-   Upgrade version.
*   Wed Nov 11 2015 Xiaolin Li <amakhalov@vmware.com> 3.6.4-1
-   Initial build
