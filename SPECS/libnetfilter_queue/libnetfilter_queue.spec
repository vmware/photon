Summary:      Provides API to packets queued by kernel packet filter
Name:         libnetfilter_queue
Version:      1.0.5
Release:      4%{?dist}
URL:          http://www.netfilter.org/projects/libnetfilter_queue/index.html
Group:        System Environment/Libraries
Vendor:       VMware, Inc.
Distribution: Photon

Source0:      http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha512  %{name}=732a44b602e5efaa4f5582ea25ff8f5ec8f4dca5c0e725cd93fe2d441db80416b25c6018147be90acb262d7428eb5b21b3f7b5920e612d115061ec6a19d67f85

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libmnl-devel
BuildRequires:  libnfnetlink-devel
BuildRequires:  linux-api-headers

%description
libnetfilter_queue is a userspace library providing an API to packets that
have been queued by the kernel packet filter. It is is part of a system that
deprecates the old ip_queue / libipq mechanism. libnetfilter_queue has been
previously known as libnfnetlink_queue.

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
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%files
%doc COPYING
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.0.5-4
- Release bump for SRP compliance
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.5-3
- Remove .la files
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 1.0.5-2
- Use autosetup and ldconfig scriptlets
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.5-1
- Automatic Version Bump
* Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 1.0.3-1
- Update to 1.0.3
* Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2-1
- Initial packaging
