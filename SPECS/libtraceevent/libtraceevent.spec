Summary:        Linux kernel trace event library
Name:           libtraceevent
Version:        1.6.3
Release:        1%{?dist}
License:        GPL-2.0 and LGPL-2.1
Group:          Development/Tools
URL:            https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/snapshot/%{name}-%{version}.tar.gz
%define sha512 %{name}=8064eb18dda6fdbff020759ed92e785b87d34be9ebc30cb6085785edeb8d7252cabf8d33d8738a3ec407672a3d891884d0f0b4c551fce26c76fa8eaf61b9e2f5

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
* Mon Nov 14 2022 Michelle Wang <michellew@vmware.com> 1.6.3-1
- Initial Version
