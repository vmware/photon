%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name terminal-table
Name:           rubygem-terminal-table
Version:        3.0.2
Release:        2%{?dist}
Summary:        Simple, feature rich ascii table generation library
Group:          Applications/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD
URL:            https://rubygems.org/gems/%{gem_name}
Source0:        https://rubygems.org/downloads/terminal-table-%{version}.gem
%define sha512    terminal-table=9d625a5903c7511f59f2e083ed2db72d337405019c41461b97590411a5028a061ce4a42eeb75c19b0e6deb2ef81f18ad80bb74d4ebdb9eca9ff6004631ddd994
BuildRequires:  ruby
Requires:       ruby
Requires:       rubygem-unicode-display_width

%description
Simple, feature rich ascii table generation library

%prep
%autosetup -c -T

%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.0.2-2
-   Bump Version to build with new ruby
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.0.2-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.8.0-2
-   Rebuilt using ruby-2.7.1
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.8.0-1
-   Update to version 1.8.0
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
