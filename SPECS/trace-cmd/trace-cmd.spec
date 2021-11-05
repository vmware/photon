Summary:        trace-cmd is a user-space front-end command-line tool for Ftrace
Name:           trace-cmd
Version:        2.9
Release:        2%{?dist}
License:        GPL-2.0 and LGPL-2.1

Group:          Development/Tools
URL:            https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/%{name}-v%{version}.tar.gz
%define sha1 trace-cmd=0938a81d44a87b672460faf2704f63fd124a172c
Patch1:         0001-trace-cmd-Add-option-to-poll-trace-buffers.patch
BuildRequires:  audit-devel
BuildRequires:  asciidoc
BuildRequires:  swig
BuildRequires:  python2-devel
BuildRequires:  docbook-xsl
BuildRequires:  libxml2-devel
BuildRequires:  libxslt
BuildRequires:  gcc
Requires:       audit python2 traceevent-plugins

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
make install install_python install_doc \
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
%{_libdir}/%{name}/python
%{_mandir}/man1/%{name}*
%{_mandir}/man5/%{name}*

%files -n traceevent-plugins
%defattr(-,root,root)
%{_libdir}/traceevent/plugins

%changelog
* Tue Oct 05 2021 Sharan Turlapati <sturlapati@vmware.com> 2.9-2
- Include --poll option to trace-cmd
* Wed Jul 22 2020 Sharan Turlapati <sturlapati@vmware.com> 2.9-1
- Initial version of trace-cmd for Photon
