%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mime-types

Name: rubygem-mime-types
Version:        3.5.2
Release:        2%{?dist}
Summary:        The mime-types library provides a library and registry for information about MIME content type definitions.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=099e3b984d3637dfeaf00a76e56427c278ce3c48b77aaa45ed63521e73b1877d773d0ebe4fbe1ec21113987f7d39cda0deeefb7c9ded5f2a3024577e3e6ab6ff

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: ruby-devel
BuildRequires: rubygem-mime-types-data

Requires: ruby
Requires: rubygem-mime-types-data >= 3.2015.0, rubygem-mime-types-data < 4.0.0

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
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.5.2-2
-   Build gems properly
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.5.2-1
-   Update to version 3.5.2
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.4.1-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.3.1-1
-   Automatic Version Bump
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.2.2-1
-   Initial build
