Summary:    User-space infrastructure for connection tracking timeout
Name:       libnetfilter_cttimeout
Version:    1.0.1
Release:    2%{?dist}
URL:        http://www.netfilter.org/projects/libnetfilter_cttimeout/index.html
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha512 libnetfilter_cttimeout=3f7886b2b8c67fb45d9f6d03f8a327d0f04072abf75ec0fa310f4a321a1749607e79b48f47c8b8488f9833734689419264afada0cbc1f0360a5ae9e17d4a1100

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libmnl-devel
BuildRequires:  linux-api-headers

%description
libnetfilter_cttimeout is the userspace library that provides the programming interface to the fine-grain connection tracking timeout infrastructure. With this library, you can create, update and delete timeout policies that can be attached to traffic flows.

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
%autosetup -n libnetfilter_cttimeout-%{version}

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
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libnetfilter_cttimeout
%{_includedir}/libnetfilter_cttimeout/*.h
%{_libdir}/*.so

%changelog
*   Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.0.1-2
-   Release bump for SRP compliance
*   Mon Dec 05 2022 Anmol Jain <anmolja@vmware.com> 1.0.1-1
-   Update to 1.0.1
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.0-1
-   Initial packaging
