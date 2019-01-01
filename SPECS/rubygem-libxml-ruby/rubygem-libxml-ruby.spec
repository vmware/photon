%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name libxml-ruby
Name:           rubygem-libxml-ruby
Version:        3.0.0
Release:        4%{?dist}
Summary:        Provides Ruby language bindings for the GNOME Libxml2 XML toolkit
Group:          Applications/Programming
License:        BSD
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}
Source0:        https://rubygems.org/downloads/libxml-ruby-%{version}.gem
%define sha1    libxml-ruby=9a4f28d019da0aef73773d676f9ba3ce9294b6bb
BuildRequires:  ruby >= 2.4.0
BuildRequires:  libxml2-devel
Requires:       ruby >= 2.4.0
%description
Provides Ruby language bindings for the GNOME Libxml2 XML toolkit
%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/libxml-ruby-%{version}
# Remove test failures that included \r\n in the given files for canonicalize tests.
sed -i "s|assert_equal|#assert_equal|g" test/tc_canonicalize.rb
gem install rake-compiler
rake test

%files
%defattr(-,root,root,-)
%{gemdir}
%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 3.0.0-4
-   Increment the release version as part of ruby upgrade
*   Thu Sep 05 2017 Chang Lee <changlee@vmware.com> 3.0.0-3
-   Added %check without canonicalize tests
*   Thu Apr 13 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.0.0-2
-   Change ruby version in buildrequires and requires
*   Wed Mar 22 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.0-1
-   Updated to version 3.0.0.
*   Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 2.8.0-3
-   Bump up release number to reflect ruby upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.8.0-2
-   GA - Bump release of all rpms
*   Wed Nov 11 2015 Anish Swaminathan <anishs@vmware.com> 2.8.0-1
-   Initial build

