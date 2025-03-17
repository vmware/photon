Summary:        Gnuplot is a portable command-line driven graphing utility.
Name:           gnuplot
Version:        5.4.5
Release:        4%{?dist}
URL:            http://www.gnuplot.info
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  lua-devel
BuildRequires:  readline-devel

Requires:       lua
Requires:       readline

%description
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. The source code is copyrighted but freely distributed (i.e., you don't have to pay for it). It was originally created to allow scientists and students to visualize mathematical functions and data interactively, but has grown to support many non-interactive uses such as web scripting. It is also used as a plotting engine by third-party applications like Octave. Gnuplot has been supported and under active development since 1986.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-shared
%make_build

%install
%make_install %{?_smp_mflags}

%check
make check %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 5.4.5-4
- Release bump for SRP compliance
* Tue Jun 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.4.5-3
- Bump version as a part of lua upgrade
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.4.5-2
- Bump version as a part of readline upgrade
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 5.4.5-1
- Automatic Version Bump
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 5.4.3-1
- Automatic Version Bump
* Wed Dec 01 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.4.2-1
- Upgrade to version 5.4.2
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 5.4.1-1
- Automatic Version Bump
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
