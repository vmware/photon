%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name nokogiri

Summary:        Nokogiri is an HTML, XML, SAX, and Reader parser.
Name:           rubygem-nokogiri
Version:        1.8.4
Release:        4%{?dist}
License:        MIT
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/nokogiri/
Source0:        https://rubygems.org/downloads/nokogiri-%{version}.gem
%define sha512  nokogiri=35ef9a4f8129abb0b5336356114be23a436f6cab0d4f3bb12f00415d64f0a2eaa7b9d746930a7198b9238ce13a1365b0de03fef54353fc071e23fec0f0cbe85d
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
%autosetup -c -T -p1
%build

%install
NOKOGIRI_USE_SYSTEM_LIBRARIES=1 gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%{_fixperms} %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Mar 10 2023 Shivani Agarwal <shivania2@vmware.com> 1.8.4-4
-   Fix file and directory permission
*   Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.8.4-3
-   Bump version as a part of libxslt upgrade
*   Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.8.4-2
-   Version bump up to use libxml2 2.9.11-4.
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
