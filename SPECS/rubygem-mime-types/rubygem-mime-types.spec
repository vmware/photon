%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mime-types

Name: rubygem-mime-types
Version:        3.4.1
Release:        2%{?dist}
Summary:        The mime-types library provides a library and registry for information about MIME content type definitions.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512    mime-types=d0cec7afbe1685c008765997c3047f23bbb0bd10989cd82475805f932e61c400b3d2e60f5f95804c46919b57f0d3644c866be358b0c4c653ace43d62bbc98e4f

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby >= 2.0

Requires: rubygem-mime-types-data >= 3.2015.0, rubygem-mime-types-data < 4.0.0
BuildArch: noarch

%description
The mime-types library provides a library and registry for information about MIME content
type definitions. It can be used to determine defined filename extensions for MIME types,
or to use filename extensions to look up the likely MIME type definitions. Version 3.0 is
a major release that requires Ruby 2.0 compatibility and removes deprecated functions. The
columnar registry format introduced in 2.6 has been made the primary format; the registry
data has been extracted from this library and put into
{mime-types-data}[https://github.com/mime-types/mime-types-data]. Additionally, mime-types
is now licensed exclusively under the MIT licence and there is a code of conduct in effect.
There are a number of other smaller changes described in the History file.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.4.1-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.4.1-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.3.1-1
-   Automatic Version Bump
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.2.2-1
-   Initial build
