%global debug_package %{nil}
%global gem_name ffi

Name:           rubygem-ffi
Version:        1.13.1
Release:        4%{?dist}
Summary:        Ruby FFI library
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD-2-Clause
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/ffi-%{version}.gem
%define sha512  ffi=4c0b5086463c5abedc440c44fb12c62612627a2aaad60b1959ea8831d4ec2bbe3217fec0b63612730bb219748fd2bd2252dd615ca0305fb7f0e8456c63c31fbd

BuildRequires:  ruby-devel
BuildRequires:  gcc
BuildRequires:  libffi-devel
BuildRequires:  gmp-devel
BuildRequires:  findutils

%description
Ruby FFI library

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.13.1-4
-   Add gem macros
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.13.1-3
-   Build from source
*   Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.13.1-2
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.13.1-1
-   Automatic Version Bump
*   Tue Sep 25 2018 Ajay Kaher <akaher@vmware.com> 1.9.25-3
-   Adding aarch64 support.
*   Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 1.9.25-2
-   Remove Provides itself and BuildArch
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.9.25-1
-   Initial build
