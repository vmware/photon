Summary:        gptfdisk-1.0.4
Name:           gptfdisk
Version:        1.0.9
Release:        4%{?dist}
URL:            http://sourceforge.net/projects/gptfdisk
Group:          System Environment/Filesystem and Disk management
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://downloads.sourceforge.net/project/gptfdisk/%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# Patch0 taken from:
# http://ftp.oregonstate.edu/.1/blfs/conglomeration/gptfdisk/gptfdisk-1.0.9-convenience-1.patch
Patch0: %{name}-%{version}-convenience-1.patch
Patch1: gptfdisk-Makefile.patch
Patch2: 0001-Updated-guid.cc-to-deal-with-minor-change-in-libuuid.patch

BuildRequires: popt-devel
BuildRequires: ncurses-devel
BuildRequires: util-linux-devel

Requires: popt >= 1.16
Requires: ncurses
Requires: ncurses-devel
Requires: libstdc++
Requires: util-linux

%description
The gptfdisk package is a set of programs for creation and maintenance of GUID Partition
Table (GPT) disk drives. A GPT partitioned disk is required for drives greater than 2 TB
and is a modern replacement for legacy PC-BIOS partitioned disk drives that use a
Master Boot Record (MBR). The main program, gdisk, has an interface similar to the
classic fdisk program.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
sed -i 's|ncursesw/||' gptcurses.cc
%make_build POPT=1

%install
%make_install %{?_smp_mflags} POPT=1
mv %{buildroot}/sbin %{buildroot}%{_usr}

%{_fixperms} %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.0.9-4
- Release bump for SRP compliance
* Wed Sep 20 2023 Oliver Kurth <okurth@vmware.com> 1.0.9-3
- add patch to fix "Unable to generate a proper UUID" error
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 1.0.9-2
- Bump version as a part of ncurses upgrade to v6.4
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.9-1
- Upgrade to v1.0.9
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.7-3
- Fix binary path
* Fri Nov 19 2021 Oliver Kurth <okurth@vmware.com> 1.0.7-2
- Build with -tinfo
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.0.7-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.5-1
- Automatic Version Bump
* Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> 1.0.4-1
- Update version to 1.0.4
* Mon Jun 05 2017 Bo Gan <ganb@vmware.com> 1.0.1-4
- Fix dependency
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.0.1-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-2
- GA - Bump release of all rpms
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.1-1
- Updated Version.
* Thu Oct 30 2014 Divya Thaluru <dthaluru@vmware.com> 0.8.10-1
- Initial build.    First version
