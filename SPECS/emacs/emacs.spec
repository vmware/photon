Summary:        GNU Emacs text editor
Name:           emacs
Version:        27.1
Release:        1%{?dist}
License:        GPLv3+ and CC0-1.0
URL:            http://www.gnu.org/software/emacs/
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.xz
%define sha1    emacs=d1b6b9efa666614c5628dda9ea78628796a73f7f

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
%autosetup

%build
./configure --prefix=/usr            \
            --localstatedir=/var     \
            --without-xpm            \
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
make

%install
make DESTDIR=%{buildroot} install

rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/icons

rm %{buildroot}%{_bindir}/ctags
rm %{buildroot}%{_datadir}/applications/emacs.desktop

%files
%defattr(-,root,root)
%{_bindir}/ebrowse
%{_bindir}/emacs
%{_bindir}/emacs-27.1
%{_bindir}/emacsclient
%{_bindir}/etags
%{_includedir}/emacs-module.h
%{_libdir}/systemd/user/emacs.service
%{_libexecdir}/emacs/27.1/x86_64-pc-linux-gnu/emacs.pdmp
%{_libexecdir}/emacs/27.1/x86_64-pc-linux-gnu/hexl
%{_libexecdir}/emacs/27.1/x86_64-pc-linux-gnu/movemail
%{_libexecdir}/emacs/27.1/x86_64-pc-linux-gnu/rcs2log
%{_datadir}/emacs/27.1/etc/*
%{_datadir}/emacs/27.1/lisp/*
%{_datadir}/emacs/27.1/site-lisp/subdirs.el
%{_datadir}/emacs/site-lisp/subdirs.el
%{_datadir}/metainfo/emacs.appdata.xml

%changelog
*  Tue Oct 06 2020 Susant Sahani <ssahani@vmware.com>  27.1-1
-  Initial rpm release.
