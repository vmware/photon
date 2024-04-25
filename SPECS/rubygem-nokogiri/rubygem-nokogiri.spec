%global debug_package   %{nil}
%global gem_name        nokogiri

Summary:        Nokogiri is an HTML, XML, SAX, and Reader parser.
Name:           rubygem-nokogiri
Version:        1.12.5
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/nokogiri/
Source0:        https://rubygems.org/downloads/nokogiri-%{version}.gem
%define sha512  nokogiri=29ef38133906f3ffc4b8a3d8f980b5b684dcab21360a46fa618cc47caf1f98f51654a64648a1cc638d784a33336f24ce45a6ea43aa365caf39702e36ab75dbcf
BuildRequires:  ruby-devel
BuildRequires:  rubygem-mini_portile2
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
Requires:       ruby >= 2.4.0
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

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.12.5-5
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.12.5-4
-   Build from source
*   Fri Mar 10 2023 Shivani Agarwal <shivania2@vmware.com> 1.12.5-3
-   Fix the Directory and file permission
*   Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.12.5-2
-   Release bump up to use libxml2 2.9.12-1.
*   Fri Oct 08 2021 Sujay G <gsujay@vmware.com> 1.12.5-1
-   Bump version to 1.12.5 to fix CVE-2021-41098
*   Tue Jul 20 2021 Sujay G <gsujay@vmware.com> 1.11.3-1
-   Bump version to 1.11.3 to fix CVE-2020-26247
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
