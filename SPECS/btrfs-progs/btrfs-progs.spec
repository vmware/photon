%global build_if %{photon_subrelease} >= 91

Name:           btrfs-progs
Version:        7.0
Release:        1%{?dist}
Summary:        Userspace programs for btrfs
Group:          System Environment/Base
URL:            http://btrfs.wiki.kernel.org/index.php/Main_Page
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  e2fsprogs-devel
BuildRequires:  libacl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  asciidoc3
BuildRequires:  systemd-devel

Requires:       e2fsprogs

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package        devel
Summary:        btrfs filesystem-specific libraries and headers
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
btrfs-progs-devel contains the libraries and header files needed to
develop btrfs filesystem-specific programs.

You should install btrfs-progs-devel if you want to develop
btrfs filesystem-specific programs.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
sh ./autogen.sh
%configure \
    --disable-zstd \
    --disable-documentation \
    --disable-lzo

make DISABLE_DOCUMENTATION=1 %{?_smp_mflags}

%install
make %{?_smp_mflags} \
     DISABLE_DOCUMENTATION=1 \
     mandir=%{_mandir} \
     bindir=%{_sbindir} \
     libdir=%{_libdir} \
     incdir=%{_includedir} \
     DESTDIR=%{buildroot} \
     install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libbtrfs.so.0*
%{_libdir}/libbtrfsutil.so.1*
%{_sbindir}/btrfsck
%{_sbindir}/fsck.btrfs
%{_sbindir}/mkfs.btrfs
%{_sbindir}/btrfs-image
%{_sbindir}/btrfs-convert
%{_sbindir}/btrfstune
%{_sbindir}/btrfs
%{_sbindir}/btrfs-map-logical
%{_sbindir}/btrfs-find-root
%{_udevrulesdir}/64-btrfs-dm.rules
%{_udevrulesdir}/64-btrfs-zoned.rules
%{_sbindir}/btrfs-select-super

%files devel
%{_includedir}/*
%exclude %{_libdir}/libbtrfs.a
%exclude %{_libdir}/libbtrfsutil.a
%{_libdir}/libbtrfs.so
%{_libdir}/libbtrfsutil.so
%{_libdir}/pkgconfig/libbtrfsutil.pc

%changelog
* Tue May 26 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.0-1
- Upgrade to v7.0
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.3-6
- Extended to build for subrelease 91 and above
* Tue Mar 31 2026 Guruswamy Baasavaiah <guruswamy.basavaiah@broadcom.com> 6.1.3-5
- Version bump for removing lzo support in btrfs-progs
* Tue Mar 31 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 6.1.3-4
- Remove stale BuildRequires: xmlto; documentation is already disabled
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.1.3-3
- Bump version as a part of python3.14 upgrade
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 6.1.3-2
- Release bump for SRP compliance
* Fri Feb 10 2023 Gerrit Photon <photon-checkins@vmware.com> 6.1.3-1
- Automatic Version Bump
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.11.1-2
- Update release to compile with python 3.11
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 5.11.1-1
- Automatic Version Bump
* Fri Jul 17 2020 Tapas Kundu <tkundu@vmware.com> 5.7-2
- Use asciidoc3
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 5.7-1
- Automatic Version Bump
* Mon Nov 19 2018 Sujay G <gsujay@vmware.com> 4.19-1
- Bump btrfs-progs version to 4.19
* Wed Sep 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.10.2-2
- Fix compilation issue againts e2fsprogs-1.44
* Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  4.10.2-1
- Upgrade to 4.10.2
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.4-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  4.4-1
- Upgrade to 4.4
* Thu Feb 26 2015 Divya Thaluru <dthaluru@vmware.com> 3.18.2-1
- Initial version
