%global build_flags prefix=%{_prefix} lib_dir=%{_libdir} libexec_dir=%{_libexecdir}/%{name} etc_dir=%{_sysconfdir}/%{name}

Summary:        Operating system utility that allows programs to run as non-previleged user.
Name:           authbind
Version:        2.1.3
Release:        3%{?dist}
URL:            http://www.chiark.greenend.org.uk/ucgi/~ian/git/authbind.git
Group:          Applications/utils
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.debian.org/debian/pool/main/a/%{name}/%{name}_%{version}.tar.gz
%define sha512 %{name}=357c8f5c5ad446e75a597d5bc5bb5af7db17de771643a39976b5ac1425f03bf44f322c8dd07b0e1b04a0bf78d5000841b4866e0d0945584689e99291156dfac1

Source1: license.txt
%include %{SOURCE1}

Patch0: 0001-adjust-makefile-to-help-build-rpms.patch

%description
The authbind software allows a program that would normally require
superuser privileges to access privileged network services to run as
a non-privileged user.

%prep
%autosetup -p1 -n work

%build
%make_build %{build_flags}

%install
%make_install %{?_smp_mflags} %{build_flags} STRIP=/bin/true

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_libdir}/libauthbind.so.*
%{_libexecdir}/%{name}/helper
%{_sysconfdir}/%{name}
%{_mandir}/*

%changelog
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2.1.3-3
- Release bump for SRP compliance
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.1.3-2
- Fix build & packaging
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.3-1
- Automatic Version Bump
* Thu Oct 22 2020 Dweep Advani <dadvani@vmware.com> 2.1.2-2
- Fixed install failure
* Fri Jul 14 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.1.2-1
- Initial build. First version
