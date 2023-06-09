Summary:        Displays information about running processes
Name:           psmisc
Version:        23.6
Release:        3%{?dist}
License:        GPLv2+
URL:            https://gitlab.com/psmisc/psmisc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://sourceforge.net/projects/%{name}/files/%{name}/%{name}-%{version}.tar.xz
%define sha512 %{name}=4daffbd1726e50d9344f8578dd4c10f0b8f7971929ec667490de31122e5f3828747e1bafb3ed3c37ed7e1758ab9ec43b8f4556b676a416a8efbc7c6c88b6985d

BuildRequires:  ncurses-devel

Requires:       ncurses

%description
The Psmisc package contains programs for displaying information about running processes.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%find_lang %{name}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*

%changelog
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 23.6-3
- Bump version as a part of ncurses upgrade to v6.4
* Wed Mar 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 23.6-2
- Fix binary path
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
