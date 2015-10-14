Summary:	Provides IPC between GnuPG Components
Name:		libassuan
Version:	2.2.0
Release:	3%{?dist}
License:	GPLv3+
URL:		https://www.gnupg.org/(fr)/related_software/libassuan/index.html
Group:		Development/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha1 libassuan=7cf0545955ce414044bb99b871d324753dd7b2e5
Requires:	libgpg-error >= 1.17
BuildRequires:	libgpg-error-devel >= 1.17
%description
The libassuan package contains an inter process communication library used by some of the other GnuPG related packages. libassuan's primary use is to allow a client to interact with a non-persistent server. libassuan is not, however, limited to use with GnuPG servers and clients. It was designed to be flexible enough to meet the demands of many transaction based environments with non-persistent servers. 
%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, header files and documentation for developing applications that use %{name}.

%prep
%setup -q
%build
./configure --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_infodir}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_datadir}/aclocal/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h

%changelog
*   Wed Oct 14 2015 Xiaolin Li <xiaolinl@vmware.com> 2.2.0-3
-   Move development libraries and header files to devel package.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.2.0-2
-   Updated group.
*	Tue Dec 30 2014 Divya Thaluru <dthaluru@vmware.com> 2.2.0-1
	Initial version
