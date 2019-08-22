%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name nio4r

Name: rubygem-nio4r
Version:        2.4.0
Release:        1%{?dist}
Summary:        Cross-platform asynchronous I/O primitives for scalable network clients and servers.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    nio4r=dbad76d9a1a7d130aebd1c6d1d5c59a0c2fcacb9
BuildRequires:  gmp-devel
BuildRequires:  ruby >= 2.3.0

BuildArch: x86_64

%description
Cross-platform asynchronous I/O primitives for scalable network clients and servers.
Inspired by the Java NIO API, but simplified for ease-of-use.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-1
-   Initial build
