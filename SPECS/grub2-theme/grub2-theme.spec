Summary:       Photon theme for grub2
Name:          grub2-theme
Version:       5.0
Release:       3%{?dist}
Group:         System Environment/Base
URL:           https://vmware.github.io/photon/
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       %{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}
BuildArch:     noarch
Conflicts: %{name}-ostree < 5.0-3

%description
grub2-theme provides content of /boot/grub2/themes/photon plus ascii font.

%prep
%autosetup -p1

%install
install -d %{buildroot}/boot
cp -a grub2 %{buildroot}/boot/
ln -s grub2 %{buildroot}/boot/grub

%files
%defattr(-,root,root,-)
/boot/grub
/boot/grub2/fonts/ascii.pf2
/boot/grub2/fonts/unicode.pf2
/boot/grub2/fonts/unifont.pf2
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
* Tue Apr 07 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 5.0-3
- Fold grub2-theme-ostree fonts into main package; drop ostree subpackage
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 5.0-2
- Release bump for SRP compliance
* Wed Jan 18 2023 Piyush Gupta <gpiyush@vmware.com> 5.0-1
- Update 5.0 Beta boot splash image.
* Tue Feb 16 2021 Anish Swaminathan <anishs@vmware.com> 4.0-2
- Update GA boot splash image.
* Mon Nov 02 2020 Alexey Makhalov <amakhalov@vmware.com> 4.0-1
- Updated boot splash image.
* Tue May 12 2020 Ankit Jain <ankitja@vmware.com> 3.2-3
- Added unicode.pf2 and unifont.pf2 to grub2/fonts folder.
* Wed Mar 11 2020 Alexey Makhalov <amakhalov@vmware.com> 3.2-2
- Move ascii.pf2 to grub2/fonts folder.
* Mon Mar 09 2020 Alexey Makhalov <amakhalov@vmware.com> 3.2-1
- Initial packaging
