Summary:        SELinux policy module utils
Name:           semodule-utils
Version:        3.4
Release:        2%{?dist}
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=3a102eb83e1feff9796c4da572500be1e3a8a8bc8a7eed762ef4144761280f0513050c714aa287b1e4e67d2938f9f9a0ee5036762472d732eae0288b437cb7a9

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libsepol-devel = %{version}
Requires:       libsepol = %{version}
Requires:       libselinux-utils

%description
semodule-utils is set of tools for SELinux policy module manipulations.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" \
     BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" %{?_smp_mflags} install
# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%files
%defattr(-,root,root,-)
%{_bindir}/semodule_expand
%{_bindir}/semodule_link
%{_bindir}/semodule_package
%{_bindir}/semodule_unpackage
%{_mandir}/man8/semodule_expand.8.gz
%{_mandir}/man8/semodule_link.8.gz
%{_mandir}/man8/semodule_package.8.gz
%{_mandir}/man8/semodule_unpackage.8.gz

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.4-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.4-1
- Upgrade v3.4
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Upgrade v3.3
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.2-1
- Automatic Version Bump
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Sun Jul 05 2020 Vikash Bansal <bvikas@vmware.com> 3.0-2
- Add libselinux-utils in requires
* Thu Apr 30 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
