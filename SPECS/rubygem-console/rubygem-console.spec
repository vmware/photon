%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name console

Summary:        Beautiful logging for Ruby.
Name:           rubygem-console
Version:        1.16.2
Release:        3%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby

Requires: ruby
Requires: rubygem-fiber-local

BuildArch: noarch

%description
Provides beautiful console logging for Ruby applications. Implements fast, buffered log output.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.16.2-3
-   Release bump for SRP compliance
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.16.2-2
-   Fix requires
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.16.2-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.0-1
-   Automatic Version Bump
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.4.0-1
-   Initial build
