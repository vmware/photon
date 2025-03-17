Summary:        Linux kernel trace file system library
Name:           libtracefs
Version:        1.5.0
Release:        2%{?dist}
Group:          Development/Tools
URL:            https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git/snapshot/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libtraceevent-devel

Requires: libtraceevent

%description
The libtracefs(3) library provides APIs to access kernel trace file system.

%package        devel
Summary:        Header files for libtracefs
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    devel
These are the header files of libtracefs.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install %{?_smp_flags} prefix=%{_prefix} libdir=%{_libdir}

%clean
rm -rf %{buildroot}

%ldconfig_scriptlets

%files
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/tracefs/*.h
%{_libdir}/%{name}.a
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.5.0-2
- Release bump for SRP compliance
* Mon Nov 14 2022 Michelle Wang <michellew@vmware.com> 1.5.0-1
- Initial Version
