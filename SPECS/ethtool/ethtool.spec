Summary:        Standard Linux utility for controlling network drivers and hardware
Name:           ethtool
Version:        5.8
Release:        2%{?dist}
License:        GPLv2
URL:            https://www.kernel.org/pub/software/network/ethtool/
Group:          Productivity/Networking/Diagnostic
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.kernel.org/pub/software/network/%{name}/%{name}-%{version}.tar.xz
%define sha1    ethtool=b16ecf0ede1635f8a8abac9b8db58b831f408f7b
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
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

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
