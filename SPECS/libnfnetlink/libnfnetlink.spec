Summary:    Library for netfilter related kernel/userspace communication
Name:       libnfnetlink
Version:    1.0.1
Release:    1%{?dist}
License:    GPLv2+
URL:        http://www.netfilter.org/projects/libnfnetlink/index.html
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha1 libnfnetlink=27ae2dfbd976e28cb7a417f9e946c901f512dd9a

BuildRequires:  linux-api-headers

%description
libnfnetlink is the low-level library for netfilter related kernel/userspace communication. It provides a generic messaging infrastructure for in-kernel netfilter subsystems (such as nfnetlink_log, nfnetlink_queue, nfnetlink_conntrack) and their respective users and/or management tools in userspace.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
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
%dir %{_includedir}/libnfnetlink
%{_includedir}/libnfnetlink/*.h
%{_libdir}/*.so

%changelog
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.1-1
-   Initial packaging

