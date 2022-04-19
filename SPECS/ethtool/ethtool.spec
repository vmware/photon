Summary:        Standard Linux utility for controlling network drivers and hardware
Name:           ethtool
Version:        5.17
Release:        1%{?dist}
License:        GPLv2
URL:            https://www.kernel.org/pub/software/network/ethtool/
Group:          Productivity/Networking/Diagnostic
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.kernel.org/pub/software/network/%{name}/%{name}-%{version}.tar.xz
%define sha512    ethtool=c9677829e3ed1f373bd993f72c710293a6e987bbd19829d437a436f42cf4e7995ee70a7db3590b1499ff6aa29c26815f4d0a3e4798ffb6992ae3f52b079cd3ff
BuildRequires:  libmnl-devel
Requires:       libmnl

%description
ethtool is the standard Linux utility for controlling network drivers and hardware,
particularly for wired Ethernet devices

%prep
%autosetup

%build
autoreconf -fi
%configure --sbindir=/sbin

# make doesn't support _smp_mflags
%make_build

%install
%make_install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%doc AUTHORS COPYING NEWS README ChangeLog
%defattr(-,root,root)
/sbin/ethtool
%{_datadir}/bash-completion/completions/ethtool
%{_mandir}

%changelog
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
