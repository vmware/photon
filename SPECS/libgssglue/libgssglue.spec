Summary:        This library exports a gssapi interface
Name:           libgssglue
Version:        0.4
Release:        4%{?dist}
URL:            http://www.citi.umich.edu/projects/nfsv4/linux/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.citi.umich.edu/projects/nfsv4/linux/libgssglue/%{name}-%{version}.tar.gz
%define sha512    libgssglue=25d514c08320e42851ff153d7691267a8454f205492faf942f566aa30c1ac1c83bd095732a1a0fcc010ba3a5d48b4c95a196ad05bc821598cc1fc3a2c4960d29

Source1: license.txt
%include %{SOURCE1}

%description
This library exports a gssapi interface, but doesn't implement any gssapi mechanisms itself; instead it calls gssapi routines in other libraries, depending on the mechanism.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}/%{_libdir} -name '*.la' -delete

%post

%files
%defattr(-,root,root)
%{_libdir}/libgssglue.so.*

%files  devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libgssglue.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.4-4
-   Release bump for SRP compliance
*   Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 0.4-3
-   Corrected spec file name
*   Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> 0.4-2
-   Resolved compilation error for aarch64
*   Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 0.4-1
-   Initial build. First version
