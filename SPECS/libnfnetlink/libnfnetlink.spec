Summary:    low-level library for netfilter related kernel/userspace communication.
Name:       libnfnetlink
Version:    1.0.1
Release:    1%{?dist}
License:    LGPLv2.1+
URL:        http://netfilter.org/projects/libnfnetlink/
Group:      System Environment/libraries
Vendor:     VMware, Inc.
Distribution: Photon
Source0:     http://netfilter.org/projects/libnfnetlink/files/%{name}-%{version}.tar.bz2
%define sha1 libnfnetlink=27ae2dfbd976e28cb7a417f9e946c901f512dd9a

BuildRequires:  linux-devel

%description
libnfnetlink is the low-level library for netfilter related kernel/userspace communication. It provides a generic messaging infrastructure for in-kernel netfilter subsystems

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       linux-devel

%description devel
Libraries and header files for libnfnetlink library.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --enable-static=no
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libnfnetlink.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libnfnetlink
%{_includedir}/libnfnetlink/*.h
%{_libdir}/*.so

%changelog
*   Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.1-1
-   Initial build.	First version
