%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name unf_ext

Name: rubygem-unf_ext
Version:        0.0.7.7
Release:        1%{?dist}
Summary:        Unicode Normalization Form support library for CRuby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    unf_ext=d0d10680d5bb965d1186ccefb6c01a35e31c4a56
BuildRequires:  ruby
BuildRequires:  gmp-devel

%description
Unicode Normalization Form support library for CRuby.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.0.7.7-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-2
-   Enabled build for non x86_64 build archs
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-1
-   Initial build
