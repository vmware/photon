Name:           cpulimit
Version:        2.8
Release:        1%{?dist}
Summary:        CPU Usage Limiter for Linux
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/System
License:        GPLv2+
URL:            https://sourceforge.net/projects/limitcpu

Source0: https://sourceforge.net/projects/limitcpu/files/limitcpu/%{name}-%{version}.tar.gz
%define sha512 %{name}=aeb121739a5dc9f94c6ddb0905ed05eb7d146c9d0e71c34ba46aad798bda2c30b7ccc548338b4c468f9885f09d97a4565c00199c8df6af74dc9b6f23940c540e

BuildRequires:  glibc-devel

Requires:       glibc

%description
cpulimit is a simple program which attempts to limit the CPU usage of a process
(expressed in percentage, not in CPU time). This is useful to control batch
jobs, when you don't want them to eat too much CPU. It does not act on the nice
value or other scheduling priority stuff, but on the real CPU usage. Also, it
is able to adapt itself to the overall system load, dynamically and quickly.

%prep
%autosetup -p1

%build
%make_build

%install
export PREFIX=%{buildroot}%{_prefix}
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man1/*

%changelog
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 2.8-1
- Automatic Version Bump
* Mon May 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2-1
- Upgrade to v1.2
- Actual tag version is 0.2 but to maintain proper versioning, using 1.2
* Tue May 10 2022 Benson Kwok <bkwok@vmware.com> 1.1-1
- Initial build. First version
