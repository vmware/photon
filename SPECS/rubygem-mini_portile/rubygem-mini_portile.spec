%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mini_portile

Name:           rubygem-mini_portile
Version:        0.6.2
Release:        5%{?dist}
Summary:        Simplistic port-like solution for developers
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/mini_portile/
Source0:        https://rubygems.org/downloads/mini_portile-%{version}.gem
%define sha512  mini_portile=fd6ce49b5db291e8216f001e4a3bd14d69a920d6d457de7566f7526abf616dad3ec86d4951ab4b881ffd185b4d4e02e64eb2ae494cd9a1275e342b78afa4e2bc

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby
Requires:       ruby
%description
Simplistic port-like solution for developers. It provides a standard and simplified way to compile against dependency libraries without messing up your system.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.6.2-5
- Release bump for SRP compliance
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.6.2-4
- Rebuilt with ruby-2.7.1
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 0.6.2-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.2-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6.2-1
- Initial build
