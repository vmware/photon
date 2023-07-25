Summary:        Noninteractive ssh password provider
Name:           sshpass
Version:        1.09
Release:        3%{?dist}
License:        GPLv2+
URL:            http://sourceforge.net/projects/sshpass/
Source0:        http://downloads.sourceforge.net/project/sshpass/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha512  sshpass=9b4ba83ca4d34364e7c43e29f98493dc3d595d24dc68c2fe3c244600d92a0f8bc0a6a7f8f43d64c0b4d714eb196516f297d904fa66035a76dae89a3726c0f2ff
Group:          Applications/Networking
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       openssh

%description
sshpass is a utility designed for running ssh using the mode referred to as "keyboard-interactive" password authentication, but in non-interactive mode.

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make prefix=%{_prefix} %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS
%{_bindir}
%{_mandir}/man1

%changelog
*       Tue Jul 25 2023 Shivani Agarwal <shivania2@vmware.com> 1.09-3
-       Bump version as part of openssh upgrade
*       Fri Jun 02 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.09-2
-       Bump version as part of openssh upgrade
*       Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.09-1
-       Automatic Version Bump
*       Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.06-1
-       Update to version 1.06
*       Tue Oct 04 2016 ChangLee <changlee@vmware.com> 1.05-4
-       Modified %check
*       Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.05-3
-       GA - Bump release of all rpms
*       Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> 1.05-2
-       Add requires for openssh
*       Fri Sep 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.05-1
-       Initial version
