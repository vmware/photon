Summary:	fork of the original IJG libjpeg which uses SIMD.
Name:		libjpeg-turbo
Version:	1.5.1
Release:	1%{?dist}
License:	IJG
URL:		http://sourceforge.net/projects/libjpeg-turbo
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/libjpeg-turbo/%{name}-%{version}.tar.gz
%define sha1 libjpeg-turbo=ebb3f9e94044c77831a3e8c809c7ea7506944622
BuildRequires:	nasm
Requires:	nasm
%description
libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to accelerate baseline JPEG compression and decompression. libjpeg is a library that implements JPEG image encoding, decoding and transcoding.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q 
%build
./configure \
	--prefix=%{_prefix} \
	--disable-static \
	--mandir=/usr/share/man \
	--with-jpeg8
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*		Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-1
-		Updated to version 1.5.1
*       Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
-       Initial version

