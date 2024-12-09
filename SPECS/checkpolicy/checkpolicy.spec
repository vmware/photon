Summary:        SELinux policy compiler
Name:           checkpolicy
Version:        3.5
Release:        2%{?dist}
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=fcd490d865af3b4350c32c5dd9916f8406219841e1e255d8945c6dcc958535247aa27af5597a6988e19f11faea7beeabcb46e8ba2431112bb4aa5c7697bca529

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libsemanage-devel = %{version}
BuildRequires:  bison

%description
checkpolicy is a program that checks and compiles a SELinux security policy configuration
into a binary representation that can be loaded into the kernel.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" \
     BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" %{?_smp_mflags} install
# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/checkmodule
%{_mandir}/man8/checkpolicy.8.gz
%{_mandir}/man8/checkmodule.8.gz

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 3.5-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.4-1
- Upgrade v3.4
* Fri Apr 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3-1
- Upgrade v3.3
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 3.2-1
- Automatic Version Bump
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Thu Apr 30 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
