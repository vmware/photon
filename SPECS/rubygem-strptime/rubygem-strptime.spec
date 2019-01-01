%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name strptime

Name: rubygem-strptime
Version:        0.2.3
Release:        2%{?dist}
Summary:        a fast strptime/strftime engine which uses VM
Group:          Development/Languages
License:        BSD 2
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/strptime-%{version}.gem
%define sha1    strptime=b4749bb078a1e89ebf2eb010ebfa54ac65112114
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
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 0.2.3-2
-   Increment the release version as part of ruby upgrade
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.2.3-1
-   Initial build
