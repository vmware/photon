Summary:        GNU Emacs text editor
Name:           emacs
Version:        30.1
Release:        1%{?dist}
License:        GPLv3+ and CC0-1.0
URL:            http://www.gnu.org/software/emacs/
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.xz
%define sha512  emacs=511a6a1d2a170a207913692e1349344b70a0b5202b8d1ae27dc7256e589c77ae9e35da16fc2a098bf9f1b8d0f60233f452ed8d6744b70b907f3484c42f2d7d7f

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  ncurses-devel
BuildRequires:  systemd-devel
BuildRequires:  gnutls-devel

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

%prep
%autosetup -p1

%build
%configure --without-xpm            \
            --without-jpeg           \
            --without-tiff           \
            --without-gif            \
            --without-png            \
            --without-rsvg           \
            --without-lcms2          \
            --without-xft            \
            --without-harfbuzz       \
            --without-m17n-flt       \
            --without-toolkit-scroll-bars \
            --without-xaw3d          \
            --without-xim            \
            --without-makeinfo
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/icons

rm %{buildroot}%{_bindir}/ctags
rm %{buildroot}%{_datadir}/applications/emacs.desktop
rm %{buildroot}%{_datadir}/applications/%{name}-mail.desktop
rm %{buildroot}%{_datadir}/applications/emacsclient-mail.desktop
rm %{buildroot}%{_datadir}/applications/emacsclient.desktop

%files
%defattr(-,root,root)
%{_bindir}/ebrowse
%{_bindir}/%{name}
%{_bindir}/%{name}-%{version}
%{_bindir}/emacsclient
%{_bindir}/etags
%{_includedir}/%{name}-module.h
%{_libdir}/systemd/user/%{name}.service
%{_libexecdir}/%{name}/%{version}/%{_arch}-unknown-linux-gnu/%{name}-*.pdmp
%{_libexecdir}/%{name}/%{version}/%{_arch}-unknown-linux-gnu/hexl
%{_libexecdir}/%{name}/%{version}/%{_arch}-unknown-linux-gnu/movemail
%{_libexecdir}/%{name}/%{version}/%{_arch}-unknown-linux-gnu/rcs2log
%{_datadir}/%{name}/%{version}/etc/*
%{_datadir}/%{name}/%{version}/lisp/*
%{_datadir}/%{name}/%{version}/site-lisp/subdirs.el
%{_datadir}/%{name}/site-lisp/subdirs.el
%{_datadir}/metainfo/%{name}.metainfo.xml

%changelog
*  Tue Apr 29 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 30.1-1
-  Version upgrade
*  Thu Feb 13 2025 Harinadh D <Harinadh.Dommaraju@broadcom.com> 29.4-1
-  Version upgrade
-  Fixes CVE-2024-30202,CVE-2024-30203,CVE-2024-30204,CVE-2024-30205
*  Mon Jul 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 27.1-6
-  Fix for CVE-2024-39331
*  Tue Nov 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 27.1-5
-  Bump version as a part of gnutls upgrade
*  Fri Mar 03 2023 Srish Srinivasan <ssrish@vmware.com> 27.1-4
-  Fix CVE-2022-48338, CVE-2022-48339, CVE-2022-48337
*  Mon Dec 05 2022 Srish Srinivasan <ssrish@vmware.com> 27.1-3
-  Fix for CVE-2022-45939
*  Fri Oct 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 27.1-2
-  Fix aarch64 build error
*  Tue Oct 06 2020 Susant Sahani <ssahani@vmware.com>  27.1-1
-  Initial rpm release.
