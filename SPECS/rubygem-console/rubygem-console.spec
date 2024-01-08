%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name console

Name: rubygem-console
Version:        1.9.0
Release:        2%{?dist}
Summary:        Beautiful logging for Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  console=e73cf7ba1213a8de4f5992326dec5db4a3fd3ef34cf235651245337e7de8e1142a0396771c43520184cca27d5f79eb481882d64629808547aa2bb5356133a65d

BuildRequires:  ruby

Requires: ruby
Requires: rubygem-fiber-local

BuildArch: noarch

%description
Provides beautiful console logging for Ruby applications. Implements fast, buffered log output.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.9.0-2
-   Initial version. Needed by rubygem-async-http.
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.0-1
-   Automatic Version Bump
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.4.0-1
-   Initial build
