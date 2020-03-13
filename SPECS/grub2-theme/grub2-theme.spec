Summary:    Photon theme for grub2
Name:       grub2-theme
Version:    3.2
Release:    2%{?dist}
License:    Apache License
Group:      System Environment/Base
URL:        https://vmware.github.io/photon/
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    %{name}-%{version}.tar.xz
%define sha1 grub2-theme=92a05137036705c5fe872489da407cf94b125cc7
BuildArch:  noarch

%description
grub2-theme provides content of /boot/grub2/themes/photon plus ascii font.

%prep
%setup -q

%install
install -d %{buildroot}/boot
cp -a grub2 %{buildroot}/boot/
ln -s grub2 %{buildroot}/boot/grub
# TODO: move fonts to proper place in source tarball
# Moving ascii to grub2/fonts will allow to load it by
# loadfont ascii
install -d %{buildroot}/boot/grub2/fonts
cp ascii.pf2 %{buildroot}/boot/grub2/fonts/

%files
%defattr(-,root,root,-)
/boot/grub
/boot/grub2/fonts/ascii.pf2
%dir /boot/grub2/themes
%dir /boot/grub2/themes/photon
/boot/grub2/themes/photon/photon.png
/boot/grub2/themes/photon/terminal_c.tga
/boot/grub2/themes/photon/terminal_e.tga
/boot/grub2/themes/photon/terminal_n.tga
/boot/grub2/themes/photon/terminal_ne.tga
/boot/grub2/themes/photon/terminal_nw.tga
/boot/grub2/themes/photon/terminal_s.tga
/boot/grub2/themes/photon/terminal_se.tga
/boot/grub2/themes/photon/terminal_sw.tga
/boot/grub2/themes/photon/terminal_w.tga
/boot/grub2/themes/photon/theme.txt

%changelog
* Wed Mar 11 2020 Alexey Makhalov <amakhalov@vmware.com> 3.2-2
- Move ascii.pf2 to grub2/fonts folder.
* Mon Mar 09 2020 Alexey Makhalov <amakhalov@vmware.com> 3.2-1
- Initial packaging
