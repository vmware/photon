Summary:	Mesos
Name:		mesos
Version:	0.23.0
Release:	1%{?dist}
License:	Apache
URL:		http://mesos.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://mirror.sdunix.com/apache/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1 mesos=05006a8a2752a089f40823d1c9ec795476ed0b93
BuildRequires:	openjdk >= 1.8.0.45
BuildRequires:	curl
BuildRequires:	apache-maven >= 3.3.3
BuildRequires:	apr >= 1.5.2
BuildRequires:	apr-util >= 1.5.4
BuildRequires:	subversion >= 1.8.13
BuildRequires:	cyrus-sasl >= 2.1.26
BuildRequires:	python2 >= 2.6
BuildRequires:	python2-libs
BuildRequires:	python2-devel
Requires:	apr >= 1.5.2
Requires:	apr-util >= 1.5.4
Requires:	cyrus-sasl >= 2.1.26
Requires:	expat
Requires:	openjdk >= 1.8.0.45
Requires:	subversion >= 1.8.13

%description
This package installs mesos services that allow photon to run tasks using mesos frameworks.

%prep
%setup -q

%build
sed -i 's/gzip -d -c $^ | tar xf -/tar --no-same-owner -xf $^/' 3rdparty/Makefile.in
sed -i 's/gzip -d -c $^ | tar xf -/tar --no-same-owner -xf $^/' 3rdparty/libprocess/3rdparty/Makefile.in
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir}
make

%check
make check

%install
make DESTDIR=%{buildroot} install

[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_includedir}/*/*
%{_sbindir}/*
%{_prefix}/etc/mesos/*
%{_libexecdir}/mesos/*
%{_datadir}/mesos/*

%changelog
*	Tue Sep 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.23.0-1
-	Update to mesos 0.23.0.
*	Fri Aug 28 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.22.1-3
-	Disable parallel build. Fix Requires.
*	Thu Jul 16 2015 Alexey Makhalov <amakhalov@vmware.com> 0.22.1-2
-	Untar with --no-same-owner to get it compilable in container.
*	Fri Jun 26 2015 Sarah Choi <sarahc@vmware.com> 0.22.1-1
-	Initial build.	First version
