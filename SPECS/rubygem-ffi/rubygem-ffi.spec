%global debug_package %{nil}
%global gem_name ffi

Name:           rubygem-ffi
Version:        1.15.5
Release:        4%{?dist}
Summary:        Ruby FFI library
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/ffi-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel
BuildRequires:  gcc
BuildRequires:  libffi-devel
BuildRequires:  gmp-devel
BuildRequires:  findutils
Requires:       ruby

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
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.15.5-4
- Release bump for SRP compliance
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.15.5-3
- Add gem macros
* Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.15.5-2
- Build from source
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.15.5-1
- Automatic Version Bump
* Wed May 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.13.1-3
- Bump version as a part of libffi upgrade
* Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.13.1-2
- Drop group write permissions for files in /usr/lib to comply with STIG
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.13.1-1
- Automatic Version Bump
* Tue Sep 25 2018 Ajay Kaher <akaher@vmware.com> 1.9.25-3
- Adding aarch64 support.
* Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 1.9.25-2
- Remove Provides itself and BuildArch
* Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.9.25-1
- Initial build
