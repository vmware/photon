Summary:        User-space infrastructure for connection tracking helpers
Name:           libnetfilter_cthelper
Version:        1.0.1
Release:        2%{?dist}
URL:            http://www.netfilter.org/projects/libnetfilter_cthelper/index.html
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libmnl-devel
BuildRequires:  linux-api-headers

%description
libnetfilter_cthelper is the userspace library that provides the programming interface to the user-space helper infrastructure available since Linux kernel 3.6. With this library, you register, configure, enable and deactivate user-space helpers.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libmnl-devel
Requires:       linux-api-headers

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%doc examples
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libnetfilter_cthelper
%{_includedir}/libnetfilter_cthelper/*.h
%{_libdir}/*.so

%changelog
*   Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.0.1-2
-   Release bump for SRP compliance
*   Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
-   Automatic Version Bump
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.0-1
-   Initial packaging
