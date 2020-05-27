Summary:	Displays information about running processes
Name:		psmisc
Version:	23.2
Release:	4%{?dist}
License:	GPLv2+
URL:		http://psmisc.sourceforge.net/
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://prdownloads.sourceforge.net/psmisc/%{name}-%{version}.tar.xz
%define sha1 psmisc=2bf3ec1c87ab3bc0610c819452c21cf4b849b0b8
%ifarch aarch64
Patch0:         peekfd_arm64.patch
%endif
BuildRequires:	ncurses-devel
Requires:	ncurses
%description
The Psmisc package contains programs for displaying information
about running processes.

%prep
%setup -q
%ifarch aarch64
%patch0 -p1
%endif

%build
./configure \
	--prefix=%{_prefix} 
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
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
* Tue Apr 23 2019 Ajay Kaher <akaher@vmware.com> 23.2-4
- Fix peekfd_arm64.patch
* Wed Mar 20 2019 Ajay Kaher <akaher@vmware.com> 23.2-3
- Add ARM64 support for peekfd
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
