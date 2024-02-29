%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-accept

Name:           rubygem-http-accept
Version:        2.2.1
Release:        1%{?dist}
Summary:        Parse Accept and Accept-Language HTTP headers.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=a23f9d84924cfe30f9b4a4ce1779392a44556e2b852b5afad37199f8d724087cfc6e418497acbf24d17393b322ab8854ccb38decf1dcbe60f1e1ad562f350030

BuildRequires:  ruby

Requires: ruby

BuildArch: noarch

%description
Parse Accept and Accept-Language HTTP headers.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.1-1
- Update to version 2.2.1
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.2.0-2
- Fix requires
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.0-1
- Automatic Version Bump
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-3
- Downgrade to 1.7.0 for rubygem-rest-client 2.1.0
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.1-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.7.0-2
- rebuilt with ruby-2.7.1
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.7.0-1
- Initial build
