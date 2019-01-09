Summary:	Fast compression and decompression library
Name:		snappy
Version:	1.1.7
Release:	2%{?dist}
License:	BSD and LGPLv2 and Sleepycat
URL:		http://code.google.com/p/snappy/
Source0:	https://github.com/google/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 snappy=1ec676b842fc96fd8a95b03c12758935e7f257b0
Group:		System/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	cmake

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
mkdir -p build/
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DBUILD_SHARED_LIBS=ON ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_datadir}/doc/snappy/
find %{buildroot} -name '*.la' -delete

%clean
rm -rf %{buildroot}

%check
cd testdata
cmake ../ && make
make test

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS
%{_lib64dir}/*.so.*
%exclude %{_lib64dir}/cmake

%files devel
%defattr(-,root,root)
%doc format_description.txt framing_format.txt
%{_includedir}/*
%{_lib64dir}/libsnappy.so

%changelog
*  Wed Jan 09 2019 Michelle Wang <michellew@vmware.com> 1.1.7-2
-  Fix make check for snappy.
*  Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> 1.1.7-1
-  Updating the version to 1.1.7.
*  Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.1.3-1
-  Initial build. First version.
