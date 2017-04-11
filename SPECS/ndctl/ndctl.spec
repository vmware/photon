Summary:	Manage "libnvdimm" subsystem devices (Non-volatile Memory)
Name:		ndctl
Version:	56
Release:	1%{?dist}
License:	GPLv2
Group:		System Environment/Base
Url:		https://github.com/pmem/ndctl
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/pmem/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 ndctl=99dbdae3609c85270dae0530aec0206e6ad36e88

BuildRequires:	asciidoc
BuildRequires:	which
BuildRequires:	xmlto
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	kmod
BuildRequires:	systemd
BuildRequires:	json-c-devel
Requires:	ndctl-devel
Requires:	daxctl-devel

%description
Utility library for managing the "libnvdimm" subsystem.  The "libnvdimm"
subsystem defines a kernel device model and control message interface for
platform NVDIMM resources.

%package	devel
Summary:	Development files for ndctl
License:	LGPLv2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n daxctl
Summary:	Manage Device-DAX instances
License:	GPLv2
Group:		System Environment/Base

%description -n daxctl
The daxctl utility provides enumeration and provisioning commands for
the Linux kernel Device-DAX facility. This facility enables DAX mappings
of performance / feature differentiated memory without need of a
filesystem.

%package -n daxctl-devel
Summary:	Development files for daxctl
License:	LGPLv2
Group:		Development/Libraries
Requires:	daxctl = %{version}-%{release}

%description -n daxctl-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}, a library for enumerating
"Device DAX" devices.  Device DAX is a facility for establishing DAX
mappings of performance / feature-differentiated memory.

%prep
%setup -q ndctl-%{version}

%build
./autogen.sh
%configure \
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
%license util/COPYING licenses/BSD-MIT licenses/CC0
%{_bindir}/ndctl
%{_libdir}/libndctl.so.*
%{_datadir}/bash-completion/

%files devel
%defattr(-,root,root)
%license COPYING
%{_includedir}/ndctl/
%{_libdir}/libndctl.so
%{_libdir}/pkgconfig/libndctl.pc

%files -n daxctl
%defattr(-,root,root)
%license util/COPYING licenses/BSD-MIT licenses/CC0
%{_bindir}/daxctl
%{_libdir}/libdaxctl.so.*

%files -n daxctl-devel
%defattr(-,root,root)
%license COPYING
%{_includedir}/daxctl/
%{_libdir}/libdaxctl.so
%{_libdir}/pkgconfig/libdaxctl.pc

%changelog
*   Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 56-1
-   Initial build.  First version
