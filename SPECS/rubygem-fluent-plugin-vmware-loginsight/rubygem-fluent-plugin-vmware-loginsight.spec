%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-vmware-loginsight

Name: rubygem-fluent-plugin-vmware-loginsight
Version:        0.1.10
Release:        2%{?dist}
Summary:        Fluent output plugin to forward logs to VMware Log Insight.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  fluent-plugin-vmware-loginsight=380f22768d608f83a21b12accc7fb3d0a2f7f969b0610e3b9cca9b2633375c4b1271065ac18646600b22f709aece843fd1b4fd2843101f4ba64d71d1266d44e3

BuildRequires:  ruby >= 2.1

Requires: rubygem-fluentd >= 0.14.10, rubygem-fluentd < 2.0.0
Requires: ruby

BuildArch: noarch

%description
Fluent output plugin to forward logs to VMware Log Insight.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue Jan 09 2024 Shivani Agrwal <shivania2@vmware.com> 0.1.10-2
-   Fixed requires
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.10-1
-   Automatic Version Bump
*   Fri Aug 23 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.1.5-1
-   Initial build
