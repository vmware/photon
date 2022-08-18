%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name jmespath

Name: rubygem-jmespath
Version:        1.6.1
Release:        1%{?dist}
Summary:        Implements JMESPath for Ruby.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/jmespath-%{version}.gem
%define sha512    jmespath=e06f6f4d47abbe552cff4055fff3841380ee8779b61c5f68b184e1acbcc588a97ad7d83225671a9f547d1077041592553f5f44649d6ceb76d369a0fc462439f3
BuildRequires:  ruby

%description
Implements JMESPath for Ruby.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.4.0-2
-   rebuilt with ruby-2.7.1
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
-   Initial build
