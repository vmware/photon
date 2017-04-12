Summary:    User-space infrastructure for connection tracking timeout
Name:       libnetfilter_cttimeout
Version:    1.0.0
Release:    1%{?dist}
License:    GPLv2+
URL:        http://www.netfilter.org/projects/libnetfilter_cttimeout/index.html
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha1 libnetfilter_cttimeout=24cba24b0371e80007be4ea0fa9d872df63b8a7a

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
%setup -q

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
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.0-1
-   Initial packaging


