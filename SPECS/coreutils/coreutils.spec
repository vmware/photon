# this is also used in toybox.spec
%define coreutils_present %{_sharedstatedir}/rpm-state/%{name}

Summary:        Basic system utilities
Name:           coreutils
Version:        9.1
Release:        6%{?dist}
URL:            http://www.gnu.org/software/coreutils
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz
# make this package to own serial console profile since it utilizes stty tool
Source1:        serial-console.sh

Source2: license.txt
%include %{SOURCE2}

# Patches are taken from:
# www.linuxfromscratch.org/patches/downloads/coreutils/
Patch0: coreutils-%{version}-i18n-1.patch

BuildRequires:  attr-devel

Requires:       gmp

Provides:       sh-utils

Conflicts:      toybox < 0.8.2-2

%description
The Coreutils package contains utilities for showing and setting
the basic system

%package lang
Summary:    Additional language files for coreutils
Group:      System Environment/Base
Requires:   %{name} = %{version}-%{release}

%description lang
These are the additional language files of coreutils.

%prep
%autosetup -p1

%build
autoreconf -fiv
export FORCE_UNSAFE_CONFIGURE=1
%configure \
    --enable-no-install-program=kill,uptime \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/man8
mv -v %{buildroot}%{_bindir}/chroot %{buildroot}%{_sbindir}
mv -v %{buildroot}%{_mandir}/man1/chroot.1 %{buildroot}%{_mandir}/man8/chroot.8
sed -i 's/\"1\"/\"8\"/1' %{buildroot}%{_mandir}/man8/chroot.8
rm -rf %{buildroot}%{_infodir}
install -vdm755 %{buildroot}%{_sysconfdir}/profile.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/

%find_lang %{name}

%if 0%{?with_check}
%check
sed -i '37,40d' tests/df/df-symlink.sh
sed -i '/mb.sh/d' Makefile
chown -Rv nobody .
env PATH="$PATH" NON_ROOT_USERNAME=nobody make -k check-root %{?_smp_mflags}
make NON_ROOT_USERNAME=nobody check %{?_smp_mflags}
%endif

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
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 9.1-6
- Release bump for SRP compliance
* Thu Aug 08 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 9.1-5
- Resolve coreutils dependency issue on bash
* Wed Jul 03 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 9.1-4
- enable xattr support
* Mon Feb 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.1-3
- Add a flag file & use it in toybox trigger
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 9.1-2
- Fix binary path
* Mon Apr 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 9.1-1
- Upgrade to v9.1
* Sat Apr 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 9.0-1
- Upgrade to v9.0
* Sun Nov 15 2020 Prashant S Chauhan <psinghchauha@vmware.com> 8.32-3
- Fix for makecheck failure added a patch
* Tue Aug 11 2020 Sujay G <gsujay@vmware,.com> 8.32-2
- Fix aarch64 build
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 8.32-1
- Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 8.30-4
- Do not conflict with toybox >= 0.8.2-2
* Fri Nov 01 2019 Alexey Makhalov <amakhalov@vmware.com> 8.30-3
- Cross compilation support
* Thu Sep 12 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 8.30-2
- Fix for makecheck failure added a patch
* Fri Sep 07 2018 Alexey Makhalov <amakhalov@vmware.com> 8.30-1
- Version update to support glibc-2.28
* Tue Aug 28 2018 Alexey Makhalov <amakhalov@vmware.com> 8.27-4
- Add serial-console profile.d script
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 8.27-3
- Added conflicts toybox
* Wed Aug 09 2017 Rongrong Qiu <rqiu@vmware.com> 8.27-2
- Fix make check for bug 1900253
* Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 8.27-1
- Upgraded to version 8.27
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.25-2
- GA - Bump release of all rpms
* Tue May 17 2016 Divya Thaluru <dthaluru@vmware.com> 8.25-1
- Updated to version 8.25
* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 8.24-1
- Updated to version 8.24
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 8.22-1
- Initial build. First version
