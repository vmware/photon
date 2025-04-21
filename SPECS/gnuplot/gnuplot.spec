Summary:        Gnuplot is a portable command-line driven graphing utility.
Name:           gnuplot
Version:        5.4.6
Release:        2%{?dist}
License:        Freeware
URL:            http://www.gnuplot.info/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha512  %{name}=a78333f7c0ed3429b24fcdeb6296e67fb760e6f8ffc0801a6b379fcb12ae7e80cebe65a2655cb3530c2a2d4083adc34060c9a7cbe67ce98b660682c0edba174b

BuildRequires:  lua-devel

Requires:       lua

Patch0: CVE-2025-31176.patch
Patch1: CVE-2025-31178.patch
Patch2: CVE-2025-31179-1.patch
Patch3: CVE-2025-31179-2.patch
Patch4: CVE-2025-31180.patch
Patch5: CVE-2025-31181.patch

%description
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. The source code is copyrighted but freely distributed (i.e., you don't have to pay for it). It was originally created to allow scientists and students to visualize mathematical functions and data interactively, but has grown to support many non-interactive uses such as web scripting. It is also used as a plotting engine by third-party applications like Octave. Gnuplot has been supported and under active development since 1986.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-shared
%make_build

%check
%if 0%{?with_check}
sed -iE '/file map_projection.dem/,+2d' demo/all.dem
GNUTERM=dumb make check %{?_smp_mflags}
%endif

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
* Mon Apr 21 2025 Mukul Sikka <mukul.sikka@broadcom.com> 5.4.6-2
- Fix CVE-2025-31176, CVE-2025-31178, CVE-2025-31179, CVE-2025-31180, CVE-2025-31181
* Thu Jul 13 2023 Shivani Agarwal <shivania2@vmware.com> 5.4.6-1
- Upgrade to 5.4.6 and fix CVE-2020-25559
* Wed Dec 01 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.4.0-3
- Add lua to Requires
* Fri May 07 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.4.0-2
- Fix CVE-2020-25412
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 5.4.0-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 5.2.8-1
- Automatic Version Bump
* Sun Nov 25 2018 Ashwin H <ashwinh@vmware.com> 5.2.4-2
- Fix %check
* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 5.2.4-1
- Update version to 5.2.4
* Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 5.0.6-1
- Update version to 5.0.6
* Tue Nov 29 2016 Xiaolin Li <xiaolinl@vmware.com> 5.0.5-1
- Add gnuplot 5.0.5 package.
