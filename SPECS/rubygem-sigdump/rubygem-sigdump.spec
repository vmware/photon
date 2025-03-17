%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name sigdump

Name: rubygem-sigdump
Version:        0.2.4
Release:        3%{?dist}
Summary:        signal handler which dumps backtrace of running threads
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/sigdump-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby
Provides: rubygem-sigdump = %{version}

%description
Setup signal handler which dumps backtrace of running threads and number
of allocated objects per class. Require 'sigdump/setup', send SIGCONT,
and see /tmp/sigdump-<pid>.log.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.4-3
-   Release bump for SRP compliance
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.2.4-2
-   rebuilt using ruby-2.7.1
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.2.4-1
-   Initial build
