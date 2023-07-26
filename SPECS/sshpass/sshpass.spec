Summary:        Noninteractive ssh password provider
Name:           sshpass
Version:        1.06
Release:        2%{?dist}
License:        GPLv2+
URL:            http://sourceforge.net/projects/sshpass/
Source0:        http://downloads.sourceforge.net/project/sshpass/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha512  sshpass=fc08fcca5aaa5e4958f16d38116d828739a5d53f8e2a83506ef78ee602941a7bfc0e3f07154dc390660df490dbdf7601e0c7ec17c68c9627d72d565e4c6717f8
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
%make_build

%install
rm -rf %{buildroot}
%make_install prefix=%{_prefix} DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS
%{_bindir}
%{_mandir}/man1

%changelog
*   Fri Jul 28 2023 Shivani Agarwal <shivania2@vmware.com> 1.06-2
-   Bump version as part of openssh upgrade
*   Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.06-1
-   Update to version 1.06
*   Tue Oct 04 2016 ChangLee <changlee@vmware.com> 1.05-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.05-3
-   GA - Bump release of all rpms
*   Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> 1.05-2
-   Add requires for openssh
*   Fri Sep 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.05-1
-   Initial version
