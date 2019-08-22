%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-io

Name: rubygem-async-io
Version:        1.25.0
Release:        1%{?dist}
Summary:        Provides support for asynchonous TCP, UDP, UNIX and SSL sockets.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    async-io=2fb2c7655b4f888fa24321ad8924945266e4cddb
BuildRequires:  ruby >= 2.3.0, ruby < 3.0.0

Requires: rubygem-async >= 1.14.0, rubygem-async < 2.0.0

BuildArch: noarch

%description
Async::IO provides builds on async and provides asynchronous wrappers for IO, Socket, and related classes.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.25.0-1
-   Initial build
