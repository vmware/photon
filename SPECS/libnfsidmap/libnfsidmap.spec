Summary:        NFS id mapping library
Name:           libnfsidmap
Version:        0.25
Release:        2%{?dist}
License:        BSD
URL:            http://www.citi.umich.edu/projects/nfsv4/linux/
Group:          System/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.citi.umich.edu/projects/nfsv4/linux/libnfsidmap/%{name}-%{version}.tar.gz
%define sha1    libnfsidmap=f52e143d33a3a8a8138be41a90f2cc956f1acea2

%description
When NFSv4 is using AUTH_GSS (which currently only supports Kerberos v5), the
NFSv4 server mapping functions MUST use secure communications.

We provide several mapping functions, configured using /etc/idmapd.conf

As of the 0.21 version of this library, mapping methods are separate
dynamically-loaded libaries.  This allows the separation of any
LDAP requirements from the main libnfsidmap library.  The main library
now basically loads and calls the functions in the method-specific
libaries.  The method libraries are expected to be named
"libnfsidmap_<method>.so", for example, "libnfsidmap_nsswitch.so".

Several methods may be specified in the /etc/idmapd.conf configuration
file.  Each method is called until a mapping is found.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications 

%prep
%setup -q
%build
%configure --prefix=/usr --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete

%post

%files
%defattr(-,root,root)
%{_libdir}/libnfsidmap.so.*
%{_libdir}/libnfsidmap/*.so

%files  devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_libdir}/libnfsidmap.so

%changelog
*   Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> 0.25-2
-   Resolved compilation error for aarch64
*   Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 0.25-1
-   Initial build. First version
