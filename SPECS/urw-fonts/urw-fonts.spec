%global fontdir %{_datadir}/fonts/default/Type1
%global catalogue /etc/X11/fontpath.d

Summary:          Free versions of the 35 standard PostScript fonts.
Name:             urw-fonts
Version:          1.0.7pre44
Release:          1%{?dist}
URL:              http://svn.ghostscript.com/ghostscript/tags/urw-fonts-1.0.7pre44/
Source:           %{name}-%{version}.tar.bz2
%define sha512    urw-fonts=63b7b7771001b2ce832b7dcbf86bc0355d84eddb16e8599185a778401af97447af9f57d06f9398f9ce0d3d04a55a262eb3e527e5dc4c552d34f08d0776bab44a
License:          GPL3
Group:            User Interface/X
Distribution:     Photon
Vendor:           VMware, Inc.
BuildArch:        noarch
Requires:         fontconfig
Requires:         xorg-fonts

%description
Free good quality versions of the 35 standard PostScript(TM) fonts,
donated under the GPL by URW++ Design and Development GmbH.
Install the urw-fonts package if you need free versions of standard
PostScript fonts.

%prep
%autosetup -p1

%install
mkdir -p %{buildroot}%{fontdir}
install -m 0644 *.afm *.pfb %{buildroot}%{fontdir}/
# Touch ghosted files
touch %{buildroot}%{fontdir}/{fonts.{dir,scale,cache-1},encodings.dir}
# Install catalogue symlink
mkdir -p %{buildroot}%{catalogue}
ln -sf %{fontdir} %{buildroot}%{catalogue}/fonts-default

%post
{
   umask 133
   mkfontscale %{fontdir} || :
   mkfontdir %{fontdir} || :
   fc-cache %{fontdir}
} &> /dev/null || :

%postun
{
   if [ "$1" = "0" ]; then
      fc-cache %{fontdir}
   fi
} &> /dev/null || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_datadir}/fonts/default
%dir %{fontdir}
%{catalogue}/fonts-default
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.dir
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.scale
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.cache-1
%ghost %verify(not md5 size mtime) %{fontdir}/encodings.dir
%{fontdir}/*.afm
%{fontdir}/*.pfb

%changelog
* Fri Feb 17 2023 Harinadh D <hdommaraju@vmware.com> - 1.0.7pre44-1
- Initial release
