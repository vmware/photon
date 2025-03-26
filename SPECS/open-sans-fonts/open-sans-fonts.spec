%global fontname    open-sans
%global fontconf    60-%{fontname}.conf
%define _fontdir    %{_datadir}/fonts/%{fontname}

%define _fontconfig_confdir %{_sysconfdir}/fonts/conf.d
%define _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail

Name:       open-sans-fonts
# Don't bump or upgrade version of this spec
# This is a special package & needs some manual effort
Version:    1.10
Release:    2%{?dist}
Summary:    Open Sans is a humanist sans-serif typeface designed by Steve Matteson
URL:        http://www.google.com/fonts/specimen/Open+Sans
Group:      System Utility
Vendor:     VMware, Inc.
Distribution: Photon

# Since the font doesn't have clear upstream, the source zip package is
# downloaded from Google Fonts. It is then converted to tar.gz.
Source0: %{name}-%{version}.tar.xz

Source1: %{name}-fontconfig.conf

Source2: license.txt
%include %{SOURCE2}

BuildArch: noarch

%description
Open Sans is a humanist sans serif typeface designed by Steve Matteson, Type
Director of Ascender Corp. This version contains the complete 897 character
set, which includes the standard ISO Latin 1, Latin CE, Greek and Cyrillic
character sets. Open Sans was designed with an upright stress, open forms and
a neutral, yet friendly appearance. It was optimized for print, web, and mobile
interfaces, and has excellent legibility characteristics in its letter forms.

%prep
%autosetup -p1

%build

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}

install -m 0755 -d \
    %{buildroot}%{_fontconfig_templatedir} \
    %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
    %{buildroot}%{_fontconfig_templatedir}/%{fontconf}

ln -sv %{_fontconfig_templatedir}/%{fontconf} \
    %{buildroot}%{_fontconfig_confdir}/%{fontconf}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_fontdir}/*
%{_fontconfig_confdir}/*
%{_fontconfig_templatedir}/*

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.10-2
- Release bump for SRP compliance
* Thu Jun 01 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.10-1
- Initial version, needed by chromium.
