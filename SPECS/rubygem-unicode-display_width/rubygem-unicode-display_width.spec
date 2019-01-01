%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name unicode-display_width

Summary:        Unicode::DisplayWidth.
Name:           rubygem-unicode-display_width
Version:        1.1.3
Release:        3%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/janlelis/unicode-display_width
Source0:        http://rubygems.org/gems/unicode-display_width-%{version}.gem
%define sha1    unicode-display_width=ffbd2f91f7cd6660d4bb13d6114c4ca16a97d032
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
gem install yard jeweler rake rspec
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.1.3-3
-   Increment the release version as part of ruby upgrade
*   Fri Jun 23 2017 Chang Lee <changlee@vmware.com> 1.1.3-2
-   Updated %check
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.1.3-1
-   Initial build
