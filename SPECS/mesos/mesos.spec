%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:	Mesos
Name:		mesos
Version:	1.5.2
Release:	2%{?dist}
License:	Apache
URL:		http://mesos.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.apache.org/dist/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1 mesos=3709a2a8093493934e4c8e0d34114fc55cf22dfc
BuildRequires:	openjre >= %{JAVA_VERSION}
BuildRequires:  openjdk >= %{JAVA_VERSION}
BuildRequires:	curl
BuildRequires:	apache-maven >= 3.3.3
BuildRequires:	apr-devel >= 1.5.2
BuildRequires:	apr >= 1.5.2
BuildRequires:	apr-util >= 1.5.4
BuildRequires:	apr-util-devel >= 1.5.4
BuildRequires:	subversion >= 1.8.13
BuildRequires:	subversion-devel >= 1.8.13
BuildRequires:	serf-devel
BuildRequires:	cyrus-sasl >= 2.1.26
BuildRequires:	python2 >= 2.6
BuildRequires:	python2-libs
BuildRequires:  python-xml
BuildRequires:	python2-devel
BuildRequires:  python-six
BuildRequires:  python-setuptools
BuildRequires:  protobuf
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-python
BuildRequires:	which
Requires:	apr >= 1.5.2
Requires:	apr-util >= 1.5.4
Requires:	cyrus-sasl >= 2.1.26
Requires:	expat
Requires:	openjre >= 1.8.0.45
Requires:	subversion >= 1.8.13


%description
 This package installs mesos services that allow photon to run tasks in mesos
 framework.

%package	devel
Summary:	Header and development files for mesos
Requires:	%{name} = %{version}-%{release}
%description    devel
 mesos-devel package contains header files, pkfconfig files, and libraries
 needed to build applications for mesos.

%package	python
Summary:	python bindings for mesos
Requires:       python2
Requires:       protobuf-python
Conflicts:      mesos-devel < 1.2.0
%description    python
 python bindings for mesos

%prep
%setup -q

%build
sed -i 's/gzip -d -c $^ | tar xf -/tar --no-same-owner -xf $^/' 3rdparty/Makefile.am
sed -i 's/gzip -d -c $^ | tar xf -/tar --no-same-owner -xf $^/' 3rdparty/libprocess/3rdparty/Makefile.am
sed -i "/xlocale.h/d" 3rdparty/stout/include/stout/jsonify.hpp

export JAVA_HOME=/usr/lib/jvm/OpenJDK-%{JAVA_VERSION}
./configure \
	CFLAGS="%{optflags} -Wno-deprecated-declarations"  \
	CXXFLAGS="%{optflags} -Wno-deprecated-declarations" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir}
make

%check
make check

%install
export JAVA_HOME=/usr/lib/jvm/OpenJDK-%{JAVA_VERSION}
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
mv %{buildroot}%{python2_sitelib}/mesos %{buildroot}/python-mesos
rm -rf %{buildroot}%{python2_sitelib}/*
mv %{buildroot}/python-mesos %{buildroot}%{python2_sitelib}/mesos
find %{buildroot}%{python2_sitelib}/mesos -name '*.pyc' -delete
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/mesos*
%exclude %{_bindir}/easy_install
%exclude %{_bindir}/easy_install-2.7
%{_sbindir}/mesos-*
%{_libdir}/libmesos*
%{_libexecdir}/mesos/mesos-*
%{_prefix}/etc/mesos/*
%{_prefix}/share/mesos/*
%{_libdir}/libload_qos_controller-*.so
%{_libdir}/libload_qos_controller.so
%{_libdir}/liblogrotate_container_logger-*.so
%{_libdir}/liblogrotate_container_logger.so
%{_libdir}/mesos/modules/libfixed_resource_estimator-*.so
%{_libdir}/mesos/modules/libfixed_resource_estimator.so
%{_libdir}/mesos/modules/libload_qos_controller-*.so
%{_libdir}/mesos/modules/libload_qos_controller.so
%{_libdir}/mesos/modules/liblogrotate_container_logger-*.so
%{_libdir}/mesos/modules/liblogrotate_container_logger.so

%files devel
%exclude %{_includedir}/mesos/slave
%{_includedir}/*
%{_libdir}/libfixed_resource_estimator*
%{_libdir}/pkgconfig/mesos.pc
%{_prefix}/etc/mesos/*
%exclude %{_libdir}/debug/

%files python
%{python2_sitelib}/mesos/*

%changelog
*       Wed Mar 20 2019 Tapas Kundu <tkundu@vmware.com> 1.5.2-2
-       Bumped up to use latest openssl
*	Wed Feb 27 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.2-1
-	Update to 1.5.2. Includes fix for CVE-2018-1330
*       Tue Jan 23 2018 Xiaolin Li <xiaolinl@vmware.com> 1.2.2-2
-       Add serf-devel to BuildRequires.
*       Tue Oct 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.2-1
-       Updated to version 1.2.2
*	Thu Sep 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-3
-	fix conflicts with mesos-0.28
*	Thu Sep 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-2
-	for python files, package only mesos python files.
*	Fri Sep 1 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-	Update to 1.2.0-1
*	Fri May 19 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.28.2-3
-	Use JAVA_VERSION macro instead of hard coding version.
*	Mon Apr 24 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.28.2-2
-	Install protobuf build and runtime depencencies.
*	Fri Jun 24 2016 Xiaolin Li <xiaolinl@vmware.com> 0.28.2-1
-	Upgraded to version 0.28.2
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.24.0-3
-	GA - Bump release of all rpms
*	Tue May 3 2016 Xiaolin Li <xiaolinl@vmware.com> 0.24.0-2
-	Add python-setuptools to build requires.
*	Fri Sep 18 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.24.0-1
-	Upgrade to mesos 0.24.0
*	Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar.com> 0.23.0-3
-	Updated the dependencies after repackaging the openjdk. 
*	Tue Sep 08 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.23.0-2
-	Move headers, pc, dev libs into devel pkg.
*	Tue Sep 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.23.0-1
-	Update to mesos 0.23.0.
*	Fri Aug 28 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.22.1-3
-	Disable parallel build. Fix Requires.
*	Thu Jul 16 2015 Alexey Makhalov <amakhalov@vmware.com> 0.22.1-2
-	Untar with --no-same-owner to get it compilable in container.
*	Fri Jun 26 2015 Sarah Choi <sarahc@vmware.com> 0.22.1-1
-	Initial build.	First version
