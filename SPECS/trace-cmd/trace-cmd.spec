Summary:        trace-cmd is a user-space front-end command-line tool for Ftrace
Name:           trace-cmd
Version:        3.1.4
Release:        6%{?dist}
License:        GPL-2.0 and LGPL-2.1
Group:          Development/Tools
URL:            https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/%{name}-v%{version}.tar.gz
%define sha512 %{name}=93ad775c1767d2a02b72386a29867c3bc141171403c152c0c4cb907da16b5ae69100924279d9529083449c1774c97c35d5b4790b188bcd4930cfa69076cef0b8

BuildRequires:  audit-devel
BuildRequires:  swig
BuildRequires:  python3-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  gcc
BuildRequires:  libtraceevent-devel
BuildRequires:  libtracefs-devel

Requires:       audit
Requires:       python3
Requires:       libtraceevent
Requires:       libtracefs
Requires:       zstd-libs

%description
trace-cmd is a user-space command line tool that makes it convenient to use
the Ftrace functionality in the kernel by providing appropriate command interfaces
to record and analyze the traces.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
%make_build

%install
%make_install %{?_smp_mflags} prefix=%{_prefix}

%clean
rm -rf %{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB README
%{_bindir}/%{name}
%{_sysconfdir}/bash_completion.d/%{name}.bash

%changelog
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 3.1.4-6
- Bump version as a part of libxml2 upgrade
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 3.1.4-5
- Bump version as a part of libxml2 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.1.4-4
- Bump version as a part of libxml2 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.1.4-3
- Bump version as a part of zstd upgrade
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.1.4-2
- Bump up version no. as part of swig upgrade
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 3.1.4-1
- Automatic Version Bump
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.9-4
- Bump version as a part of libxslt upgrade
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9-3
- Bump version as a part of libxslt upgrade
* Tue Nov 02 2021 Sharan Turlapati <sturlapati@vmware.com> 2.9-2
- Include --poll option to trace-cmd
* Thu Oct 29 2020 Sharan Turlapati <sturlapati@vmware.com>  2.9-1
- Initial version of trace-cmd for Photon
