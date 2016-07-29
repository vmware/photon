Summary:	Library and support programs to encode and decode images in WebP format.
Name:		libwebp
Version:	0.5.1
Release:	1
License:	BSD-3-Clause
URL:		https://developers.google.com/speed/webp/?hl=en
Group:		Development/Libraries/C and C++
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz
%define sha1 libwebp=66efb2213015ad3460bef64b4fb218fdc10ce83f
Provides:	pkgconfig(libwebp)
%description
The libwebp package contains a library and support programs to encode and decode images in WebP format. 
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
*	Fri Jul 29 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.5.1-1
-	initial version
