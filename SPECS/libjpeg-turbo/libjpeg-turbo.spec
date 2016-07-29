Summary:	fork of the original IJG libjpeg which uses SIMD.
Name:		libjpeg-turbo
Version:	1.5.0
Release:	1
License:	IJG
URL:		http://sourceforge.net/projects/libjpeg-turbo
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://vmware.bintray.com/vivace_sources/0.1/%{name}-%{version}.tar.gz
%define sha1 libjpeg-turbo=9adc21b927e48e4c6889e77079f6c1f3eecf98ab
BuildRequires:	nasm
%description
libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to accelerate baseline JPEG compression and decompression. libjpeg is a library that implements JPEG image encoding, decoding and transcoding.
%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q 
%build
./configure --prefix=%{_prefix} --disable-static \
                   --mandir=/usr/share/man \
		   --with-jpeg8     
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
*	Thu Jul 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.0-1
-	Initial version
