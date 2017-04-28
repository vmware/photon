Summary:        Mesos
Name:           mesos
Version:        1.2.0
Release:        1%{?dist}
License:        Apache
URL:            http://mesos.apache.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.apache.org/dist/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1    mesos=1d570504498c90697b690e3b221feba63d0a800b
Patch0:         mesos-sysmacros.patch
BuildRequires:  openjre >= 1.8.0.45
BuildRequires:  openjdk >= 1.8.0.45
BuildRequires:  curl-devel
BuildRequires:  apache-maven >= 3.3.3
BuildRequires:  apr-devel >= 1.5.2
BuildRequires:  apr >= 1.5.2
BuildRequires:  apr-util >= 1.5.4
BuildRequires:  apr-util-devel >= 1.5.4
BuildRequires:  subversion >= 1.8.13
BuildRequires:  subversion-devel >= 1.8.13
BuildRequires:  cyrus-sasl >= 2.1.26
BuildRequires:  python2 >= 2.6
BuildRequires:  python2-libs
BuildRequires:  python-xml
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  sqlite-devel
Requires:       apr >= 1.5.2
Requires:       apr-util >= 1.5.4
Requires:       cyrus-sasl >= 2.1.26
Requires:       expat
Requires:       openjre >= 1.8.0.45
Requires:       subversion >= 1.8.13


%description
 This package installs mesos services that allow photon to run tasks in mesos
 framework.

%package    devel
Summary:    Header and development files for mesos
Requires:   %{name} = %{version}
%description    devel
 mesos-devel package contains header files, pkfconfig files, and libraries
 needed to build applications for mesos.

%prep
%setup -q
%patch0 -p1

%build
sed -i 's/gzip -d -c $^ | tar xf -/tar --no-same-owner -xf $^/' 3rdparty/Makefile.am
sed -i 's/gzip -d -c $^ | tar xf -/tar --no-same-owner -xf $^/' 3rdparty/libprocess/3rdparty/Makefile.am
./configure \
    CFLAGS="%{optflags} -Wno-deprecated-declarations"  \
    CXXFLAGS="%{optflags} -Wno-deprecated-declarations -Wno-strict-aliasing" \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir}
make

%check
make %{?_smp_mflags} check

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
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
%{_includedir}/*
%{_libdir}/libfixed_resource_estimator*
%{_libdir}/pkgconfig/mesos.pc
%{_libdir}/python2.7/site-packages/*
%{_prefix}/etc/mesos/*
%exclude %{_libdir}/debug/

%changelog
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 1.2.0-1
-   Update package version
*   Fri Mar 24 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-3
-   Added mesos-sysmacros.patch and -Wno-strict-aliasing CPPFLAGS
    to fix build issues with glibc-2.25
*   Thu Dec 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.0-2
-   BuildRequires curl-devel.
*   Tue Dec 13 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.0-1
-   Updated to version 1.1.0
*   Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 0.28.2-3
-   Use sqlite-{devel,libs}
*   Mon Oct 03 2016 ChangLee <changlee@vmware.com> 0.28.2-2
-   Modified check
*   Fri Jun 24 2016 Xiaolin Li <xiaolinl@vmware.com> 0.28.2-1
-   Upgraded to version 0.28.2
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.24.0-3
-   GA - Bump release of all rpms
*   Tue May 3 2016 Xiaolin Li <xiaolinl@vmware.com> 0.24.0-2
-   Add python-setuptools to build requires.
*   Fri Sep 18 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.24.0-1
-   Upgrade to mesos 0.24.0
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar.com> 0.23.0-3
-   Updated the dependencies after repackaging the openjdk. 
*   Tue Sep 08 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.23.0-2
-   Move headers, pc, dev libs into devel pkg.
*   Tue Sep 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.23.0-1
-   Update to mesos 0.23.0.
*   Fri Aug 28 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.22.1-3
-   Disable parallel build. Fix Requires.
*   Thu Jul 16 2015 Alexey Makhalov <amakhalov@vmware.com> 0.22.1-2
-   Untar with --no-same-owner to get it compilable in container.
*   Fri Jun 26 2015 Sarah Choi <sarahc@vmware.com> 0.22.1-1
-   Initial build. First version
