Summary:        trace-cmd is a user-space front-end command-line tool for Ftrace
Name:           trace-cmd
Version:        2.9
Release:        1%{?dist}
License:        GPL-2.0 and LGPL-2.1

Group:          Development/Tools
URL:            https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git
Source0:        https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/%{name}-v%{version}.tar.gz
%define sha1 trace-cmd=0938a81d44a87b672460faf2704f63fd124a172c
Vendor:         VMware, Inc.
Distribution:   Photon
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
%setup -q -n %{name}-v%{version}

%build
make %{?_smp_mflags} \
	prefix=%{_prefix} etcdir=%{_sysconfdir} DESTDIR=%{buildroot}

%install
make install\
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
* Thu Oct 29 2020 Sharan Turlapati <sturlapati@vmware.com>  2.9-1
- Initial version of trace-cmd for Photon
