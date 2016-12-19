Summary:	Fast compression and decompression library
Name:		snappy
Version:	1.1.3
Release:	1%{?dist}
License:	BSD and LGPLv2 and Sleepycat
URL:		http://code.google.com/p/snappy/	
Source0:	https://github.com/google/snappy/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha1 snappy=63f7a3d2c865a6a39aca9bc5d3412a8b2d607bb4
Group:		System/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon

%description
Snappy is a compression/decompression library. It does not aim for maximum 
compression, or compatibility with any other compression library; instead, it 
aims for very high speeds and reasonable compression. For instance, compared to 
the fastest mode of zlib, Snappy is an order of magnitude faster for most 
inputs, but the resulting compressed files are anywhere from 20% to 100% 
bigger.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q 

%build
./configure \
	--prefix=%{_prefix} \
	--disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%clean
rm -rf %{buildroot}

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%doc format_description.txt framing_format.txt
%{_includedir}/snappy*.h
%{_libdir}/libsnappy.so

%changelog
*	Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.1.3-1
-	Initial build. First version
