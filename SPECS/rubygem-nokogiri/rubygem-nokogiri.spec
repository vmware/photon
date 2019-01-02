%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name nokogiri

Name:           rubygem-nokogiri
Version:        1.7.1
Release:        3%{?dist}
Summary:        Nokogiri is an HTML, XML, SAX, and Reader parser.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/nokogiri/
Source0:        https://rubygems.org/downloads/nokogiri-%{version}.gem
%define sha1    nokogiri=5731c2d494381be8440f6ace6e5fcb62e7850581
BuildRequires:  ruby >= 2.4.0
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
%setup -q -c -T
%build

%install
NOKOGIRI_USE_SYSTEM_LIBRARIES=1 gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue Jan 29 2019 Srinidhi Rao <srinidhir@vmware.com> 1.7.1-3
-   Increment the release version as part of ruby upgrade.
*   Thu Sep 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.1-2
-   Build with ruby 2.4.2.
*   Wed Mar 22 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.1-1
-   Updated to version 1.7.1.
*   Tue Jan 31 2017 Anish Swaminathan <anishs@vmware.com> 1.6.7.2-5
-   Take dependency on ruby version
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

