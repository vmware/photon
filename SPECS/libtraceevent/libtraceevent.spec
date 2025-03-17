Summary:        Linux kernel trace event library
Name:           libtraceevent
Version:        1.6.3
Release:        2%{?dist}
Group:          Development/Tools
URL:            https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/snapshot/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
The libtraceevent(3) library provides APIs to access kernel tracepoint events, located in the tracefs file system under the events directory.

%package        devel
Summary:        Header files for libtraceevent
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    devel
These are the header files of libtraceevent.

%package -n traceevent-plugins
Summary:    traceevent-plugins
Group:      System/Tools
Conflicts:  linux-tools < 4.19.138-4

%description -n traceevent-plugins
traceevent-plugins

%prep
%autosetup -p1

%build
%make_build

%install
%make_install %{?_smp_flags} libdir=%{_libdir} prefix=%{_prefix}

%clean
rm -rf %{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/libtraceevent.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/traceevent/*.h
%{_libdir}/libtraceevent.a
%{_libdir}/libtraceevent.so
%{_libdir}/pkgconfig/libtraceevent.pc

%files -n traceevent-plugins
%defattr(-,root,root)
%{_libdir}/traceevent/plugins/*.so

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.6.3-2
- Release bump for SRP compliance
* Mon Nov 14 2022 Michelle Wang <michellew@vmware.com> 1.6.3-1
- Initial Version
