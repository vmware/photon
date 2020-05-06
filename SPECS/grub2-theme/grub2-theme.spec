Summary:    Photon theme for grub2
Name:       grub2-theme
Version:    3.2
Release:    3%{?dist}
License:    Apache License
Group:      System Environment/Base
URL:        https://vmware.github.io/photon/
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    %{name}-%{version}p1.tar.xz
%define sha1 grub2-theme=3fee3f9d516958e00fcb2b9ceb957327ede15605
BuildArch:  noarch

%description
grub2-theme provides content of /boot/grub2/themes/photon plus ascii font.

%package ostree
Summary: GRUB fonts for Ostree
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
%description ostree
GRUB fonts required by Ostree

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
# Required for ostree in efi boot
cp unicode.pf2 %{buildroot}/boot/grub2/fonts/
cp unifont.pf2 %{buildroot}/boot/grub2/fonts/

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

%files ostree
%defattr(-,root,root,-)
/boot/grub2/fonts/unicode.pf2
/boot/grub2/fonts/unifont.pf2

%changelog
* Tue May 12 2020 Ankit Jain <ankitja@vmware.com> 3.2-3
- Added unicode.pf2 and unifont.pf2 to grub2/fonts folder.
* Wed Mar 11 2020 Alexey Makhalov <amakhalov@vmware.com> 3.2-2
- Move ascii.pf2 to grub2/fonts folder.
* Mon Mar 09 2020 Alexey Makhalov <amakhalov@vmware.com> 3.2-1
- Initial packaging
