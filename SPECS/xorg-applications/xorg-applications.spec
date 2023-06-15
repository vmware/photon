Summary:        The Xorg applications.
Name:           xorg-applications
Version:        7.7
Release:        5%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/app/bdftopcf-1.1.tar.bz2
%define sha512 bdftopcf=7b790e8d512ca2812ac889c156ef91c48798b4744a6857e5b17e0128764b5afa8c5426fe5de05a9819d64745116718db4221b3e657e3c2633465e87179c44bec

Source1: http://ftp.x.org/pub/individual/app/mkfontdir-1.0.7.tar.bz2
%define sha512 mkfontdir=96d1920565514f90621e18a87fb5a2db9e052d1bffc6552d9659e065a21e252ab98b4e62013755032b98ed6d8c3381eb75c3c8e02651766ee4791ca622dcef1f

Source2: http://ftp.x.org/pub/individual/app/mkfontscale-1.2.2.tar.gz
%define sha512 mkfontscale=3cb40a6c04f817157507f05cf8641d5cc8cf7b858b87c13cc7fdd7cb15627f3cfb7bf5b344107baeea2348705cbf718e2bf9cd7d19a0978d9ffd5867edc5ee17

BuildRequires:  libX11-devel
BuildRequires:  libXfont2-devel

Requires:       libX11
Requires:       libXfont2

%description
The Xorg applications provide the expected applications available in previous X Window implementations.

%prep
# Using autosetup is not feasible
%setup -q -c %{name}-%{version} -a0 -a1 -a2

%build
for pkg in `ls` ; do
    pushd $pkg
    case $pkg in
      luit-[0-9]* )
        line1="#ifdef _XOPEN_SOURCE"
        line2="#  undef _XOPEN_SOURCE"
        line3="#  define _XOPEN_SOURCE 600"
        line4="#endif"

        sed -i -e "s@#ifdef HAVE_CONFIG_H@$line1\n$line2\n$line3\n$line4\n\n&@" sys.c
        unset line1 line2 line3 line4
      ;;
      sessreg-* )
        sed -e 's/\$(CPP) \$(DEFS)/$(CPP) -P $(DEFS)/' -i man/Makefile.in
      ;;
    esac
    %configure
    %make_build
    popd
done

%install
for pkg in `ls` ; do
    pushd $pkg
    %make_install %{?_smp_mflags}
    popd
done

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 7.7-5
- Bump version as a part of libX11 upgrade
* Wed Jan 11 2023 Shivani Agarwal <shivania2@vmware.com> 7.7-4
- Updated mkfontscale
* Fri Nov 18 2022 Shivani Agarwal <shivania2@vmware.com> 7.7-3
- Added bdftopcf, mkfontdir, mkfontscale
* Wed Nov 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 7.7-2
- Updated build requires & requires to build with Photon 2.0
* Wed May 20 2015 Alexey Makhalov <amakhalov@vmware.com> 7.7-1
- initial version
