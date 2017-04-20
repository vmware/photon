Summary:    Netfilter conntrack userspace library
Name:       libnetfilter_conntrack
Version:    1.0.6
Release:    1%{?dist}
License:    GPLv2+
URL:        http://www.netfilter.org/projects/libnetfilter_conntrack/index.html
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha1 libnetfilter_conntrack=015f985a8e171889a67769ba02d070eca53bac07

BuildRequires:  libmnl-devel
BuildRequires:  libnfnetlink-devel
BuildRequires:  linux-api-headers

%description
libnetfilter_conntrack is a userspace library providing a programming interface (API) to the in-kernel connection tracking state table. The library libnetfilter_conntrack has been previously known as libnfnetlink_conntrack and libctnetlink. 
%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libnfnetlink-devel
Requires:       linux-api-headers

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static --disable-rpath
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
%dir %{_includedir}/libnetfilter_conntrack
%{_includedir}/libnetfilter_conntrack/*.h
%{_libdir}/*.so

%changelog
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.6-1
-   Initial packaging


