Summary:        GNU Emacs text editor
Name:           emacs
Version:        27.1
Release:        4%{?dist}
License:        GPLv3+ and CC0-1.0
URL:            http://www.gnu.org/software/emacs/
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.xz
%define sha512  emacs=dfb26531d2c19cf9fb56505f03d799654b45e5f9528e777900e8280ed2c1d21e04c52f510528e31e015977c471ae63164cedee6174b7439ebcf479a21fc18064

# CVE:
Patch0: CVE-2022-45939.patch
Patch1: CVE-2022-48338.patch
Patch2: CVE-2022-48339.patch
Patch3: CVE-2022-48337.patch
Patch4: CVE-2024-39331.patch

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  ncurses-devel
BuildRequires:  systemd-devel
BuildRequires:  gnutls-devel

Requires:       gnutls
Requires:       systemd
Requires:       ncurses

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

%prep
%autosetup -p1

%build
%configure  --without-xpm            \
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

%files
%defattr(-,root,root)
%{_bindir}/ebrowse
%{_bindir}/emacs
%{_bindir}/emacs-%{version}
%{_bindir}/emacsclient
%{_bindir}/etags
%{_includedir}/emacs-module.h
%{_libdir}/systemd/user/emacs.service
%{_libexecdir}/emacs/%{version}/%{_arch}-unknown-linux-gnu/emacs.pdmp
%{_libexecdir}/emacs/%{version}/%{_arch}-unknown-linux-gnu/hexl
%{_libexecdir}/emacs/%{version}/%{_arch}-unknown-linux-gnu/movemail
%{_libexecdir}/emacs/%{version}/%{_arch}-unknown-linux-gnu/rcs2log
%{_datadir}/emacs/%{version}/etc/*
%{_datadir}/emacs/%{version}/lisp/*
%{_datadir}/emacs/%{version}/site-lisp/subdirs.el
%{_datadir}/emacs/site-lisp/subdirs.el
%{_datadir}/metainfo/emacs.appdata.xml

%changelog
*  Mon Jul 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 27.1-4
-  Fix CVE-2024-39331
*  Fri Mar 03 2023 Srish Srinivasan <ssrish@vmware.com> 27.1-3
-  Fix CVE-2022-48338, CVE-2022-48339, CVE-2022-48337
*  Mon Dec 05 2022 Srish Srinivasan <ssrish@vmware.com> 27.1-2
-  Fix for CVE-2022-45939
*  Mon Nov 09 2020 Susant Sahani <ssahani@vmware.com>  27.1-1
-  Initial rpm release.
