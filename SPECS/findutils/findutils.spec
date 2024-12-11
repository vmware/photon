Summary:    This package contains programs to find files
Name:       findutils
Version:    4.9.0
Release:    4%{?dist}
URL:        http://www.gnu.org/software/findutils
Group:      Applications/File
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://ftp.gnu.org/gnu/findutils/%{name}-%{version}.tar.xz
%define sha512 %{name}=ba4844f4403de0148ad14b46a3dbefd5a721f6257c864bf41a6789b11705408524751c627420b15a52af95564d8e5b52f0978474f640a62ab86a41d20cf14be9

Source1: license.txt
%include %{SOURCE1}

Conflicts:      toybox < 0.8.2-2

%description
These programs are provided to recursively search through a
directory tree and to create, maintain, and search a database
(often faster than the recursive find, but unreliable if the
database has not been recently updated).

%package lang
Summary: Additional language files for findutils
Group:   Applications/File
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of findutils

%prep
%autosetup -p1

%build
#make some fixes required by glibc-2.28:
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' gl/lib/*.c
sed -i '/unistd/a #include <sys/sysmacros.h>' gl/lib/mountlist.c
echo "#define _IO_IN_BACKUP 0x100" >> gl/lib/stdio-impl.h

CFLAGS="${CFLAGS:--O2 -g}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:--O2 -g}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:--O2 -g }" ; export FFLAGS ;
FCFLAGS="${FCFLAGS:--O2 -g }" ; export FCFLAGS ;
LDFLAGS="${LDFLAGS:-}" ; export LDFLAGS;

sh ./configure --host=%{_arch}-unknown-linux-gnu --build=%{_arch}-unknown-linux-gnu \
    --program-prefix= \
    --disable-dependency-tracking \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --localstatedir=%{_sharedstatedir}/locate \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
sed -i 's/find:=${BINDIR}/find:=\/usr\/bin/' %{buildroot}%{_bindir}/updatedb
rm -rf %{buildroot}%{_infodir}

%find_lang %{name}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/find
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/*/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.9.0-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.9.0-3
- Release bump for SRP compliance
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.9.0-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 4.9.0-1
- Automatic Version Bump
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 4.8.0-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 4.7.0-1
- Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-6
- Do not conflict with toybox >= 0.8.2-2
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-5
- Fix compilation issue against glibc-2.28
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 4.8.0-4
- Added conflicts toybox
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 4.8.0-3
- Add lang package.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.8.0-2
- GA - Bump release of all rpms
* Tue Apr 26 2016 Anish Swaminathan <anishs@vmware.com> 4.8.0-1
- Updated to version 4.8.0
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.4.2-1
- Initial build. First version.
