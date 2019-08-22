%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name timers

Name: rubygem-timers
Version:        4.3.0
Release:        1%{?dist}
Summary:        Schedule procs to run after a certain time, or at periodic intervals, using any API that accepts a timeout.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    timers=950a7007118d21093c01ff91f427d134408544a8
BuildRequires:  ruby >= 2.2.1

BuildArch: noarch

%description
Schedule procs to run after a certain time, or at periodic intervals, using any API that accepts a timeout.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri May 29 2020 Stanislav Hadjiiski <hadjiiskis@vmware.com> 4.3.0-1
-   Initial build
