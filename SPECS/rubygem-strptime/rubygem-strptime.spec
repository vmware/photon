%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name strptime

Name: rubygem-strptime
Version:        0.2.4
Release:        1%{?dist}
Summary:        a fast strptime/strftime engine which uses VM
Group:          Development/Languages
License:        BSD 2
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/strptime-%{version}.gem
%define sha1    strptime=71cc865de8002a43ff9a3002bdfde3241ecc3f9b
BuildRequires:  ruby
Provides: rubygem-strptime = %{version}

%description
a fast strptime/strftime engine which uses VM

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.4-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.2.3-1
-   Initial build
