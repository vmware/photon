Summary:        Standard Linux utility for controlling network drivers and hardware
Name:           ethtool
Version:        6.1
Release:        1%{?dist}
License:        GPLv2
URL:            https://www.kernel.org/pub/software/network/ethtool
Group:          Productivity/Networking/Diagnostic
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.kernel.org/pub/software/network/%{name}/%{name}-%{version}.tar.xz
%define sha512 %{name}=6ca478ec75dae7cc347b859802e1965e6c78310ec4b276dec29bdf76d3464e4186c6e5ed0cb8f013171d6c0562c1156cb0442419f5b947c314e8b91ad9fd2d93

BuildRequires:  libmnl-devel

Requires:       libmnl

%description
ethtool is the standard Linux utility for controlling network drivers and hardware,
particularly for wired Ethernet devices

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%files
%doc AUTHORS COPYING NEWS README ChangeLog
%defattr(-,root,root)
%{_sbindir}/ethtool
%{_datadir}/bash-completion/completions/ethtool
%{_mandir}/*

%changelog
* Wed Dec 21 2022 Susant Sahani <ssahani@vmware.com> 6.1-1
- Version bump
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 6.0-1
- Automatic Version Bump
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.19-1
- Upgrade to v5.19
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.17-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 5.17-1
- Automatic Version Bump
* Tue Jan 11 2022 Susant Sahani <ssahani@vmware.com> 5.15-1
- Version bump
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 5.12-1
- Automatic Version Bump
* Sat Jan 23 2021 Susant Sahani <ssahani@vmware.com> 5.10-1
- Version bump
* Sun Oct 11 2020 Prashant S Chauhan <psinghchauha@vmware.com> 5.8-2
- Add libmnl as requires by ethtool. Fixes issue while
- installing ethtool as Build Requires in python3-ethtool
* Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.8-1
- Automatic Version Bump
* Wed May 06 2020 Susant Sahani <ssahani@vmware.com> 5.4-1
- Version update
* Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> 4.18-1
- Version update
* Mon Apr 03 2017 Chang Lee <changlee@vmware.com> 4.8-1
- Upgraded to version 4.8
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2-3
- GA - Bump release of all rpms
* Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.2-2
- Change file packaging.
* Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2-1
- Initial build. First version
