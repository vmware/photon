%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name io-console

Name: rubygem-io-console
Version:        0.8.2
Release:        2%{?dist}
Summary:        Console interface for Ruby
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/io-console/versions/%{version}
Source0:        https://rubygems.org/downloads/io-console-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: gcc

Requires: ruby

%description
IO::Console provides very simple and portable access to console.
It doesn't provide higher layer features, such like curses and readline.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.8.2-2
- Extended to build for subrelease 91 and above
* Tue Jan 27 2026 Mukul Sikka <mukul.sikka@broadcom.com> 0.8.2-1
- Initial build for reline dependency
