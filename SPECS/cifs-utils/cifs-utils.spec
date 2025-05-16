Summary:        cifs client utils
Name:           cifs-utils
Version:        6.13
Release:        3%{?dist}
License:        GPLv3
URL:            http://wiki.samba.org/index.php/LinuxCIFS_utils
Group:          Applications/Nfs-utils-client
Source0:        https://ftp.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-%{version}.tar.bz2
%define sha512  cifs-utils=1337ac4b69f0c3e8d0241eb608207ba81dfa35f84c661649d25da78637882c4d73467b0f632be0bd120362e0b786e40eb340bffcf21c8a09629c441100fd10de
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libcap-ng-devel
BuildRequires:  libtalloc-devel
Requires:       libcap-ng
# fix for CVE-2022-27239
Patch0:         0001-CVE-2022-27239_mount_cifs_fix_length_check_for_ip_option_parsing.patch
# fix for CVE-2022-29869
Patch1:         0001-mount.cifs_fix_verbose_messages_on_option_parsing.patch

%description
Cifs-utils, a package of utilities for doing and managing mounts of the Linux CIFS filesystem.

%package devel
Summary:        The libraries and header files needed for Cifs-Utils development.
Group:          Development/Libraries
Requires:       cifs-utils = %{version}-%{release}

%description devel
Provides header files needed for Cifs-Utils development.

%prep
%autosetup -p1

%build
%configure \
    ROOTSBINDIR=/usr/sbin \
    --disable-pam \
    --disable-systemd &&
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/mount.cifs
%{_sbindir}/mount.smb3

%files devel
%defattr(-,root,root)
%{_includedir}/cifsidmap.h

%changelog
* Fri May 16 2025 Michelle Wang <michelle.wang@broadcom.com> 6.13-3
- Update due to libtalloc bump up to 2.4.1 required by samba-client 4.19.3
- samba-client bump up to 4.19.3 for CVE-2023-5568 and CVE-2018-14628
* Wed Jun 01 2022 Ajay Kaher <akaher@vmware.com> 6.13-2
- Fix for CVE-2022-27239, CVE-2022-29869
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 6.13-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 6.11-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 6.10-1
- Automatic Version Bump
* Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 6.8-1
- Upgraded to version 6.8
* Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 6.7-1
- Upgraded to version 6.7
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.4-2
- GA - Bump release of all rpms
* Mon Jan 25 2016 Divya Thaluru <dthaluru@vmware.com> 6.4-1
- Initial build. First version
