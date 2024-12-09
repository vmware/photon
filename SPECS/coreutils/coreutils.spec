# this is also used in toybox.spec
%define coreutils_present    %{_sharedstatedir}/rpm-state/%{name}

Summary:        Basic system utilities (SELinux enabled)
Name:           coreutils
Version:        9.1
Release:        7%{?dist}
License:        GPLv3
URL:            http://www.gnu.org/software/coreutils
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz
%define sha512 %{name}=a6ee2c549140b189e8c1b35e119d4289ec27244ec0ed9da0ac55202f365a7e33778b1dc7c4e64d1669599ff81a8297fe4f5adbcc8a3a2f75c919a43cd4b9bdfa

# make this package to own serial console profile since it utilizes stty tool
Source1: serial-console.sh

# Patches are taken from:
# www.linuxfromscratch.org/patches/downloads/coreutils/
Patch0: %{name}-%{version}-i18n-1.patch

BuildRequires: attr-devel
Requires: gmp

Provides: sh-utils = %{version}-%{release}
Provides: %{name}-selinux = %{version}-%{release}

Obsoletes: %{name}-selinux

%define ExtraBuildRequires libselinux-devel

%description
SELinux enabled coreutils package.

%package lang
Summary:    Additional language files for coreutils
Group:      System Environment/Base
Requires:   %{name} = %{version}-%{release}
Provides:   %{name}-selinux-lang = %{version}-%{release}
Obsoletes:  %{name}-selinux-lang

%description lang
These are the additional language files of coreutils.

%prep
%autosetup -p1

%build
autoreconf -fiv
export FORCE_UNSAFE_CONFIGURE=1
%configure \
    --enable-no-install-program=kill,uptime \
    --with-selinux \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/man8
mv -v %{buildroot}%{_bindir}/chroot %{buildroot}%{_sbindir}
mv -v %{buildroot}%{_mandir}/man1/chroot.1 %{buildroot}%{_mandir}/man8/chroot.8
sed -i 's/\"1\"/\"8\"/1' %{buildroot}%{_mandir}/man8/chroot.8
rm -rf %{buildroot}%{_infodir}
install -vdm755 %{buildroot}%{_sysconfdir}/profile.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/

%find_lang %{name}

%check
sed -i '/tests\/misc\/sort.pl/d' Makefile
sed -i 's/test-getlogin$(EXEEXT)//' gnulib-tests/Makefile
sed -i 's/PET/-05/g' tests/misc/date-debug.sh
sed -i 's/2>err\/merge-/2>\&1 > err\/merge-/g' tests/misc/sort-merge-fdlimit.sh
sed -i 's/)\" = \"10x0/| head -n 1)\" = \"10x0/g' tests/split/r-chunk.sh
sed  -i '/mb.sh/d' Makefile
chown -Rv nobody .

env PATH="$PATH" NON_ROOT_USERNAME=nobody \
%make_build -k check-root

%make_build check NON_ROOT_USERNAME=nobody

%clean
rm -rf %{buildroot}/*

%posttrans
mkdir -p %{_sharedstatedir}/rpm-state
touch %{coreutils_present}

%postun
[ $1 = 0 ] && rm -f %{coreutils_present} || :

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/serial-console.sh
%{_libexecdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Tue Nov 19 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 9.1-7
- Add libselinux-devel to ExtraBuildRequires
- Enable xattr support
- Rename to coreutils
* Mon Aug 12 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 9.1-6
- Resolve coreutils-selinux dependency issue on bash
* Fri Feb 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.1-5
- Add lang sub package
* Wed Jan 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.1-4
- Add a flag file & use it in toybox trigger
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 9.1-3
- Fix binary path
* Mon Apr 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 9.1-1
- Upgrade to v9.1
* Sat Apr 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 9.0-1
- Upgrade to v9.0
* Thu Aug 13 2020 Shreenidhi Shedi <sshedi@vmware.com> 8.32-2
- Fixed aarch64 build issue
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 8.32-1
- Automatic Version Bump
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 8.30-3
- coreutils-selinux: new package, cloned from coreutils.
- keep version-release in sync with coreutils.
