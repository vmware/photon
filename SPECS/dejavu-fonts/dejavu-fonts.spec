%global fontsdir %{_docdir}/packages/dejavu-fonts
%global ttfdir %{_datadir}/fonts/truetype

Summary:        The DejaVu fonts are a font family based on the Vera Fonts.
Name:           dejavu-fonts
Version:        2.37
Release:        2%{?dist}
URL:            https://dejavu-fonts.github.io/Download.html
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://sourceforge.net/projects/dejavu/files/dejavu/%{version}/dejavu-fonts-ttf-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}
BuildArch:      noarch

%description
The DejaVu font set is based on the “Bitstream Vera” fonts. Its
purpose is to provide a wider range of characters, while maintaining the
original style, using an open collaborative development process.
DejaVu contains a lot of mathematical and other symbols, arrows, braille patterns, etc

%prep
%autosetup -n %{name}-ttf-%{version}

%build

%install
mkdir -p %{buildroot}%{fontsdir}/fontconfig %{buildroot}%{ttfdir}
install -m 0755 fontconfig/* %{buildroot}%{fontsdir}/fontconfig/
install -m 0755 ttf/* %{buildroot}%{ttfdir}
install -m 0755 status.txt unicover.txt LICENSE README.md %{buildroot}%{fontsdir}

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%{fontsdir}/fontconfig/*
%{ttfdir}/*
%{fontsdir}/*

%changelog
*   Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.37-2
-   Release bump for SRP compliance
*   Thu Jun 15 2023 Harinadh D <hdommaraju@vmware.com> 2.37-1
-   Initial release
