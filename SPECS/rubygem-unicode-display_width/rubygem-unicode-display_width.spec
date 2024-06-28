%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name unicode-display_width

Summary:        Unicode::DisplayWidth.
Name:           rubygem-unicode-display_width
Version:        2.3.0
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/janlelis/unicode-display_width
Source0:        http://rubygems.org/gems/unicode-display_width-%{version}.gem
%define sha512  unicode-display_width=5c8b5cad378baee9a449d1f06edccbea12f26f8d269ba39ef500dfc6bd5c0b478aa9e0a7262ac07ad3f3e75ee66bbcd4b2d450eae78ac67a3c912804ae9ae1ec
BuildRequires:  ruby
Requires:       ruby

%description
Determines the monospace display width of a string in Ruby. Implementation based on EastAsianWidth.txt and other data, 100% in Ruby. Other than wcwidth(), which fulfills a similar purpose, it does not rely on the OS vendor to provide an up-to-date method for measuring string width.

%prep
%autosetup -c -T

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
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
-   Automatic Version Bump
*   Thu Nov 22 2018 Sujay G <gsujay@vmware.com> 1.4.0-2
-   Updated %check
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.4.0-1
-   Update to version 1.4.0
*   Fri Jun 23 2017 Chang Lee <changlee@vmware.com> 1.1.3-2
-   Updated %check
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.1.3-1
-   Initial build
