%global debug_package   %{nil}
%global gem_name        nokogiri
%global gemdir          %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})

Summary:        Nokogiri is an HTML, XML, SAX, and Reader parser.
Name:           rubygem-nokogiri
Version:        1.13.9
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/nokogiri/
Source0:        https://rubygems.org/downloads/nokogiri-%{version}.gem
%define sha512  nokogiri=207161fcf74aa1d1550841765268746e72d74b7516b34daf61cc5e7dc6af8fec4866f2734cd53afaf17fc546c92c3709a72f9e72da13071f65465855abf89bfa
BuildRequires:  ruby >= 2.4.0
BuildRequires:  rubygem-mini_portile2
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
Requires:       ruby
Requires:       rubygem-mini_portile2
Requires:       libxml2
Requires:       libxslt

%description
Nokogiri is an HTML, XML, SAX, and Reader parser. Among Nokogiri's many features is the ability to search documents via XPath or CSS3 selectors.

%prep
%autosetup -c -T -p1

%build

%install
NOKOGIRI_USE_SYSTEM_LIBRARIES=1 gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%{_fixperms} %{buildroot}/*

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.13.9-5
-   Bump version as a part of libxml2 upgrade
*   Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.13.9-4
-   Bump version as a part of libxml2 upgrade
*   Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.13.9-3
-   Bump version as a part of libxml2 upgrade
*   Fri Mar 10 2023 Shivani Agarwal <shivania2@vmware.com> 1.13.9-2
-   Fix the Directory and file permission
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.13.9-1
-   Automatic Version Bump
*   Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.10.9-3
-   Bump version as a part of libxslt upgrade
*   Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 1.10.9-2
-   Release bump up to use libxml2 2.9.12-1.
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.10.9-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.8.4-1
-   Update to version 1.8.4
*   Thu Apr 13 2017 Siju Maliakkal <smaliakkal@vmware.com> 1.7.1-2
-   Change ruby version in buildrequires and requires
*   Wed Mar 22 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.1-1
-   Updated to version 1.7.1.
*   Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 1.6.7.2-4
-   Bump up release number to reflect ruby upgrade
*   Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 1.6.7.2-3
-   Use SYSTEM_LIBRARIES for nokogiri
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.7.2-2
-   GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 1.6.7.2-1
-   Upgrade version.
*   Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.6.6.2-1
-   Initial build
