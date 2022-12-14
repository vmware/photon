Summary:        Displays information about running processes
Name:           psmisc
Version:        23.6
Release:        1%{?dist}
License:        GPLv2+
URL:            http://psmisc.sourceforge.net/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://prdownloads.sourceforge.net/psmisc/%{name}-%{version}.tar.xz
%define sha512  psmisc=4daffbd1726e50d9344f8578dd4c10f0b8f7971929ec667490de31122e5f3828747e1bafb3ed3c37ed7e1758ab9ec43b8f4556b676a416a8efbc7c6c88b6985d
BuildRequires:  ncurses-devel
Requires:       ncurses

%description
The Psmisc package contains programs for displaying information about running processes.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/fuser   %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/killall %{buildroot}/bin

%find_lang %{name}

%check
make %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
/bin/*
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 23.6-1
- Automatic Version Bump
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 23.5-1
- Automatic Version Bump
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 23.4-1
- Automatic Version Bump
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 23.3-1
- Automatic Version Bump
* Tue Oct 2 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 23.2-2
- Updated the tarball for v23.2
* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 23.2-1
- Version update to fix compilation issue againts glibc-2.28
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 22.21-5
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 22.21-4
- GA - Bump release of all rpms
* Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> 22.21-3
- Add patch for incorrect fclose in pstree
* Fri Mar 11 2016 Kumar Kaushik <kaushikk@vmware.com> 22.21-2
- Adding patch for type in fuser binary.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> 22.21-1
- Update version
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 22.20-1
- Initial build. First version
