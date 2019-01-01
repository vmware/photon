%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name terminal-table
Name:           rubygem-terminal-table
Version:        1.7.3
Release:        3%{?dist}
Summary:        Simple, feature rich ascii table generation library
Group:          Applications/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD
URL:            https://rubygems.org/gems/%{gem_name}
Source0:        https://rubygems.org/downloads/terminal-table-%{version}.gem
%define sha1    terminal=f1c4f71bcfc43d5b65016383403205b3bac9291e
BuildRequires:  ruby
Requires:       ruby
Requires:       rubygem-unicode-display_width
%description
Simple, feature rich ascii table generation library
%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}
%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.7.3-3
-   Increment the release version as part of ruby upgrade
*   Wed Mar 29 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.3-2
-   Added rubygem-unicode-display_width to requires.
*   Wed Mar 22 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.3-1
-   Updated to version 1.7.3.
*   Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 1.5.2-3
-   Bump up release number to reflect ruby upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.2-2
-   GA - Bump release of all rpms
*   Wed Nov 11 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.2-1
-   Initial build

