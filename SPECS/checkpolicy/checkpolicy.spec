Summary:        SELinux policy compiler
Name:           checkpolicy
Version:        3.1
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Libraries
Source0:        https://github.com/SELinuxProject/selinux/releases/download/20200710/%{name}-%{version}.tar.gz
%define sha1    checkpolicy=502a865ea91eedbe40f6304937c89b0c3b7475dd
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libsemanage-devel = %{version}

%description
checkpolicy is a program that checks and compiles a SELinux security policy configuration
into a binary representation that can be loaded into the kernel.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="/%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" install
# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%files
%defattr(-,root,root,-)
%{_bindir}/checkpolicy
%{_bindir}/checkmodule
%{_mandir}/man8/checkpolicy.8.gz
%{_mandir}/man8/checkmodule.8.gz

%changelog
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Thu Apr 30 2020 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build.
