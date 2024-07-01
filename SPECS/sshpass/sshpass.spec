Summary:        Noninteractive ssh password provider
Name:           sshpass
Version:        1.10
Release:        2%{?dist}
License:        GPLv2+
URL:            http://sourceforge.net/projects/sshpass/
Source0:        http://downloads.sourceforge.net/project/sshpass/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=d0fbceb956baee79803fec8bd9a2e0d1e342cbc90fb8bb4baa5a01914f870393f43bd07b62aa1da208318b4971005b9bbccf0e926c590124de11a272169db81d
Group:          Applications/Networking
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       openssh-clients

%description
sshpass is a utility designed for running ssh using the mode referred to as "keyboard-interactive" password authentication, but in non-interactive mode.

%prep
%autosetup

%build

%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS
%{_bindir}
%{_mandir}/man1

%changelog
* Mon Jul 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.10-2
- Bump version as a part of openssh upgrade
* Fri Sep 22 2023 Oliver Kurth <okurth@vmware.com> 1.10-1
- update to 1.10
- require openssh-clients instead of openssh
* Tue Jul 25 2023 Shivani Agarwal <shivania2@vmware.com> 1.09-3
- Bump version as part of openssh upgrade
* Fri Jun 02 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.09-2
- Bump version as part of openssh upgrade
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.09-1
- Automatic Version Bump
* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.06-1
- Update to version 1.06
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 1.05-4
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.05-3
- GA - Bump release of all rpms
* Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> 1.05-2
- Add requires for openssh
* Fri Sep 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.05-1
- Initial version
