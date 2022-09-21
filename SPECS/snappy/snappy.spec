Summary:	Fast compression and decompression library
Name:		snappy
Version:	1.1.8
Release:	2%{?dist}
License:	BSD and LGPLv2 and Sleepycat
URL:		http://code.google.com/p/snappy
Group:		System/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon

Source0: https://github.com/google/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=efe18ff1b3edda1b4b6cefcbc6da8119c05d63afdbf7a784f3490353c74dced76baed7b5f1aa34b99899729192b9d657c33c76de4b507a51553fa8001ae75c1c

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
Requires:	%{name} = %{version}-%{release}
%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%cmake \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install
rm -rf %{buildroot}%{_docdir}/%{name}
find %{buildroot} -name '*.la' -delete

%clean
rm -rf %{buildroot}

%if 0%{?with_check}
%check
cd %{__cmake_builddir}
make test %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS
%{_libdir}/*.so.*
%exclude %{_libdir}/cmake

%files devel
%defattr(-,root,root)
%doc format_description.txt framing_format.txt
%{_includedir}/*
%{_libdir}/libsnappy.so

%changelog
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.8-2
- Use cmake macros
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.8-1
- Automatic Version Bump
* Wed Jan 09 2019 Michelle Wang <michellew@vmware.com> 1.1.7-2
- Fix make check for snappy.
* Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> 1.1.7-1
- Updating the version to 1.1.7.
* Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.1.3-1
- Initial build. First version.
