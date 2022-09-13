Summary:        trace-cmd is a user-space front-end command-line tool for Ftrace
Name:           trace-cmd
Version:        2.9
Release:        3%{?dist}
License:        GPL-2.0 and LGPL-2.1

Group:          Development/Tools
URL:            https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/%{name}-v%{version}.tar.gz
%define sha512  trace-cmd=a37390e7ad29c9e7a97e5e7792505fe96a3802d6ea103e7c0f362a7b8cc29a102d483ec1a883b632fd9e0e7297f17866ae5eac59c825f08a8068b431a8f819e1
Patch1:         0001-trace-cmd-Add-option-to-poll-trace-buffers.patch
BuildRequires:  audit-devel
BuildRequires:  swig
BuildRequires:  python3-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt
BuildRequires:  gcc
Requires:       audit python3 traceevent-plugins

%description
trace-cmd is a user-space command line tool that makes it convenient to use
the Ftrace functionality in the kernel by providing appropriate command interfaces
to record and analyze the traces.

%package -n traceevent-plugins
Summary:    This package contains shared-libraries used by trace-cmd
Group:      System/Tools
Conflicts:  linux-tools < 4.19.138-4
%description -n traceevent-plugins
This package contains the shared-libraries used by trace-cmd as well as
other packages in the distro. The libraries include the plugins placed
in the traceevent/ directory.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
make %{?_smp_mflags} \
	prefix=%{_prefix} etcdir=%{_sysconfdir} DESTDIR=%{buildroot}

%install
make %{?_smp_mflags} install\
	             prefix=%{_prefix} etcdir=%{_sysconfdir} DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post   -p /sbin/ldconfig
%post   -n traceevent-plugins -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun -n traceevent-plugins -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB README
%{_bindir}/trace-cmd
%{_sysconfdir}/bash_completion.d/trace-cmd.bash

%files -n traceevent-plugins
%defattr(-,root,root)
%{_libdir}/traceevent/plugins

%changelog
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9-3
- Bump version as a part of libxslt upgrade
* Tue Nov 02 2021 Sharan Turlapati <sturlapati@vmware.com> 2.9-2
- Include --poll option to trace-cmd
* Thu Oct 29 2020 Sharan Turlapati <sturlapati@vmware.com>  2.9-1
- Initial version of trace-cmd for Photon
