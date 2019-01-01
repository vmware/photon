%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name sigdump

Name: rubygem-sigdump
Version:        0.2.4
Release:        2%{?dist}
Summary:        signal handler which dumps backtrace of running threads
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/sigdump-%{version}.gem
%define sha1    sigdump=12056f5de99a6117dbbd9a34135f41ebc8d71f66
BuildRequires:  ruby
Provides: rubygem-sigdump = %{version}

%description
Setup signal handler which dumps backtrace of running threads and number
of allocated objects per class. Require 'sigdump/setup', send SIGCONT,
and see /tmp/sigdump-<pid>.log.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 0.2.4-2
-   Increment the release version as part of ruby upgrade
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.2.4-1
-   Initial build
