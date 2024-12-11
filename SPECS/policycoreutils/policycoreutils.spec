Summary:        SELinux policy core utilities
Name:           policycoreutils
Version:        3.4
Release:        2%{?dist}
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=ded0d6fb5e3f165a893ee42411ac82616ddf37a02acaca6a8437b8f10ea12e5594bbd7bc7e3ead12df00c018078950f3fbe55604c41b0554257c4ca18f55ebb6

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libsemanage-devel = %{version}

Requires:       libsemanage = %{version}

%description
policycoreutils contains the policy core utilities that are required for
basic operation of a SELinux system.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" \
     BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" %{?_smp_mflags} install

rm -rf %{buildroot}%{_datadir}/locale \
       %{buildroot}%{_mandir}/ru

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/*
%{_sysconfdir}/sestatus.conf
%{_datadir}/bash-completion/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.4-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.4-1
- Upgrade v3.4
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Upgrade v3.3
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.2-1
- Automatic Version Bump
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Sat Apr 18 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
