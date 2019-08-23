%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name netrc

Name: rubygem-netrc
Version:        0.11.0
Release:        1%{?dist}
Summary:        This library can read and update netrc files, preserving formatting including comments and whitespace.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    netrc=bc59d9f86c0bd26862d6b169405c61e75bfc25f3
BuildRequires:  ruby

BuildArch: noarch

%description
This library can read and update netrc files, preserving formatting including comments and whitespace.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri May 29 2020 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.11.0-1
-   Initial build
