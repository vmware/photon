%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ffi

Name:           rubygem-ffi
Version:        1.15.5
Release:        1%{?dist}
Summary:        Ruby FFI library
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD-2-Clause
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/ffi-%{version}.gem
%define sha512  ffi=074df34edffc7038ab08199350a97b32280d61ea15dd85d459b008bd3363ec5403b4e533621c8e460e5288f01fec944bff9b149851b819e85bab75ad2362227c

BuildRequires:  ruby > 2.1.0
BuildRequires:  gcc
BuildRequires:  libffi-devel
BuildRequires:  gmp-devel
BuildRequires:  findutils
Requires:       ruby

%description
Ruby FFI library

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
[ -d %{buildroot}/usr/lib ] && find %{buildroot}/usr/lib -type f -perm /022 -exec chmod go-w {} \;

%files
%defattr(-,root,root,-)
%{gemdir}
%exclude %{_libdir}/ruby/gems/2.5.0/gems/ffi-1.9.25/ext/ffi_c/libffi-%{_arch}-linux/include/ffitarget.h

%changelog
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
