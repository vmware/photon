%{!?_udevdir: %define _udevdir /usr/lib/udev/}
Summary:        Manage "libnvdimm" subsystem devices (Non-volatile Memory)
Name:           ndctl
Version:        71
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Base
Url:            https://github.com/pmem/ndctl
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/pmem/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1    ndctl=97e9ee6a5fd8b432b6c87dd5e7dfe28f9bb9e8bf
BuildRequires:  asciidoc3
BuildRequires:  which
BuildRequires:  xmlto
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  kmod-devel
BuildRequires:  systemd-devel
BuildRequires:  json-c-devel
BuildRequires:  keyutils-devel

%description
Utility library for managing the "libnvdimm" subsystem.  The "libnvdimm"
subsystem defines a kernel device model and control message interface for
platform NVDIMM resources.

%package        devel
Summary:        Development files for ndctl
License:        LGPLv2
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n     daxctl
Summary:        Manage Device-DAX instances
License:        GPLv2
Group:          System Environment/Base

%description -n daxctl
The daxctl utility provides enumeration and provisioning commands for
the Linux kernel Device-DAX facility. This facility enables DAX mappings
of performance / feature differentiated memory without need of a
filesystem.

%package -n     daxctl-devel
Summary:        Development files for daxctl
License:        LGPLv2
Group:          Development/Libraries
Requires:       daxctl = %{version}-%{release}

%description -n daxctl-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}, a library for enumerating
"Device DAX" devices.  Device DAX is a facility for establishing DAX
mappings of performance / feature-differentiated memory.

%prep
%setup -q ndctl-%{version}

%build
./autogen.sh
%configure --with-bash=no \
    --disable-static  \
    --enable-local    \
    --disable-docs
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/ndctl
%{_libdir}/libndctl.so.*
%{_sysconfdir}/ndctl/monitor.conf
%{_unitdir}/ndctl-monitor.service
%{_sysconfdir}/modprobe.d/nvdimm-security.conf
%{_sysconfdir}/ndctl/keys/keys.readme
%{_datadir}/daxctl/daxctl.conf

%files devel
%defattr(-,root,root)
%license COPYING
%{_includedir}/ndctl/
%{_libdir}/libndctl.so
%{_libdir}/pkgconfig/libndctl.pc

%files -n daxctl
%defattr(-,root,root)
%{_bindir}/daxctl
%{_libdir}/libdaxctl.so.*

%files -n daxctl-devel
%defattr(-,root,root)
%license COPYING
%{_includedir}/daxctl/
%{_libdir}/libdaxctl.so
%{_libdir}/pkgconfig/libdaxctl.pc

%changelog
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 71-1
-   Automatic Version Bump
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 69-1
-   Automatic Version Bump
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 62-2
-   Use asciidoc3
*   Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 62-1
-   Upgrade to v62
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 56-3
-   Add kmod-devel to BuildRequires
*   Mon Apr 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 56-2
-   Removing the Requires section
*   Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 56-1
-   Initial build.  First version

