%global debug_package   %{nil}
%global gem_name        nokogiri

Summary:        Nokogiri is an HTML, XML, SAX, and Reader parser.
Name:           rubygem-nokogiri
Version:        1.16.2
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/nokogiri/
Source0:        https://rubygems.org/downloads/nokogiri-%{version}.gem
%define sha512  nokogiri=4a973610855ef9ac5cced69cd43cf723273f23dbf14586021ffaa8787b0c54fb3d63f94239636166bdeb8668d6e67d269899ebc1ad0a232d95389aeee8dad642
BuildRequires:  ruby-devel
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
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.16.2-2
-   Add gem macros
*   Tue Apr 02 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.16.2-1
-   Update to version 1.16.2
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
