%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name unicode-display_width

Summary:        Unicode::DisplayWidth.
Name:           rubygem-unicode-display_width
Version:        1.4.0
Release:        2%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/janlelis/unicode-display_width
Source0:        http://rubygems.org/gems/unicode-display_width-%{version}.gem
%define sha1    unicode-display_width=a00ac98ae5d5a065b9b12eb040a8ea792b7a8acc
BuildRequires:  ruby
Requires:       ruby

%description
Determines the monospace display width of a string in Ruby. Implementation based on EastAsianWidth.txt and other data, 100% in Ruby. Other than wcwidth(), which fulfills a similar purpose, it does not rely on the OS vendor to provide an up-to-date method for measuring string width.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/unicode-display_width-%{version}
gem install yard jeweler rake rspec unicode-emoji
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Nov 22 2018 Sujay G <gsujay@vmware.com> 1.4.0-2
-   Updated %check
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.4.0-1
-   Update to version 1.4.0
*   Fri Jun 23 2017 Chang Lee <changlee@vmware.com> 1.1.3-2
-   Updated %check
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.1.3-1
-   Initial build
