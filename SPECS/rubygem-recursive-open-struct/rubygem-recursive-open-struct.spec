%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name recursive-open-struct

Name: rubygem-recursive-open-struct
Version:        1.0.0
Release:        1%{?dist}
Summary:        A subclass of OpenStruct that allows nested hashes to be treated in a recursive fashion
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    recursive-open-struct=eec2cb6ea49881828b0941f72ad12e3047f5e5be
BuildRequires:  ruby

BuildArch: noarch

%description
RecursiveOpenStruct is a subclass of OpenStruct. It differs from OpenStruct
in that it allows nested hashes to be treated in a recursive fashion.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri May 29 2020 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.0.0-1
-   Initial build
