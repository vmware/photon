Summary:	contains libraries for reading and writing PNG files.
Name:		libpng
Version:	1.6.23
Release:	1
License:	libpng
URL:		http://www.libpng.org/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/libpng/%{name}-%{version}.tar.xz
%define sha1 libpng=4857fb8dbd5ca7ddacc40c183e340b9ffa34a097
Provides:	pkgconfig(libpng)
%description
The libpng package contains libraries used by other programs for reading and writing PNG files. The PNG format was designed as a replacement for GIF and, to a lesser extent, TIFF, with many improvements and extensions and lack of patent problems.
%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q 
%build
./configure --prefix=%{_prefix} --disable-static
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug/
%exclude %{_libdir}/*.la
%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.la
%{_datadir}/*
%changelog
*	Thu Jul 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.6.23-1
-	Initial version
