Summary:        GNU Emacs text editor
Name:           emacs
Version:        28.1
Release:        1%{?dist}
License:        GPLv3+ and CC0-1.0
URL:            http://www.gnu.org/software/emacs/
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.xz
%define sha512  emacs=c146ff7086aba49fa6c18adf4e485a59eb4c6525fddb9d385034446830b8bb0ac9e6fb76e7b6d94a9fddc41643415f36acad57a1ae16a841c97f61bc211459d9

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
%configure \
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
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/icons

rm %{buildroot}%{_bindir}/ctags
rm %{buildroot}%{_datadir}/applications/*.desktop

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
%{_datadir}/metainfo/emacs.metainfo.xml

%changelog
*  Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 28.1-1
-  Automatic Version Bump
*  Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 27.2-1
-  Automatic Version Bump
*  Fri Oct 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 27.1-2
-  Fix aarch64 build error
*  Tue Oct 06 2020 Susant Sahani <ssahani@vmware.com>  27.1-1
-  Initial rpm release.
