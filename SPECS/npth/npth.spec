Summary:	The New GNU Portable Threads Library.
Name:		npth
Version:	1.3
Release:	1%{?dist}
License:	GPLv2+ and LGPLv3+
URL:		https://github.com/gpg/npth
Group:		System Environment/Libraries.
Source0:        https://github.com/gpg/%{name}/archive/%{name}-%{version}.tar.gz 
%define sha1 npth=d82a2db3c3687a427c39c741616e71be98fd351b
Vendor:		VMware, Inc.
Distribution:	Photon

%description
This is a library to provide the GNU Pth API and thus a non-preemptive threads implementation.
In contrast to GNU Pth, it is based on the system's standard threads implementation. 
This allows the use of libraries which are not compatible to GNU Pth.  
Experience with a Windows Pth emulation showed that this is a solid way to provide
a co-routine based framework.

%package devel
Summary:       GNU npth development header and libraries.
Group:         Development/Libraries.
Requires:      npth = %{version}

%description devel
Development package for npth.

%prep
%setup -qn npth-%{name}-%{version}

%build
./autogen.sh
./configure --disable-static \
           --prefix=%{_prefix}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/aclocal/*

%changelog
*       Mon Jul 31 2017 Kumar Kaushik <kaushikk@vmware.com> 1.3-1
-       Initial Build.
