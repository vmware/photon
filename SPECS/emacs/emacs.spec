Summary:        GNU Emacs text editor
Name:           emacs
Version:        28.2
Release:        1%{?dist}
License:        GPLv3+ and CC0-1.0
URL:            http://www.gnu.org/software/emacs
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/gnu/emacs/%{name}-%{version}.tar.xz
%define sha512 %{name}=a7cec7e3e82367815a1442f69af54102dbfc434069810a9dec5938a6660cb8b076e6f1fb0bfff9695b15603dbbe05eb9c7dfd92e90cf40fc4d1e5746bce83bd8

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
%configure \
            --without-xpm \
            --without-jpeg \
            --without-tiff \
            --without-gif \
            --without-png \
            --without-rsvg \
            --without-lcms2 \
            --without-xft \
            --without-harfbuzz \
            --without-m17n-flt \
            --without-toolkit-scroll-bars \
            --without-xaw3d \
            --without-xim \
            --without-makeinfo

%make_build

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_infodir} \
       %{buildroot}%{_mandir} \
       %{buildroot}%{_datadir}/icons \
       %{buildroot}%{_bindir}/ctags \
       %{buildroot}%{_datadir}/applications/*.desktop

%files
%defattr(-,root,root)
%{_bindir}/ebrowse
%{_bindir}/%{name}
%{_bindir}/%{name}-%{version}
%{_bindir}/emacsclient
%{_bindir}/etags
%{_includedir}/%{name}-module.h
%{_libdir}/systemd/user/%{name}.service
%{_libexecdir}/%{name}/%{version}/%{_arch}-unknown-linux-gnu/%{name}.pdmp
%{_libexecdir}/%{name}/%{version}/%{_arch}-unknown-linux-gnu/hexl
%{_libexecdir}/%{name}/%{version}/%{_arch}-unknown-linux-gnu/movemail
%{_libexecdir}/%{name}/%{version}/%{_arch}-unknown-linux-gnu/rcs2log
%{_datadir}/%{name}/%{version}/etc/*
%{_datadir}/%{name}/%{version}/lisp/*
%{_datadir}/%{name}/%{version}/site-lisp/subdirs.el
%{_datadir}/%{name}/site-lisp/subdirs.el
%{_datadir}/metainfo/%{name}.metainfo.xml

%changelog
* Tue Nov 01 2022 Susant Sahani <ssahani@vmware.com> 28.2-1
- Bump version
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 28.1-2
- Bump version as a part of gnutls upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 28.1-1
- Automatic Version Bump
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 27.2-1
- Automatic Version Bump
* Fri Oct 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 27.1-2
- Fix aarch64 build error
* Tue Oct 06 2020 Susant Sahani <ssahani@vmware.com>  27.1-1
- Initial rpm release.
