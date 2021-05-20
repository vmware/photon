Summary:        Google's data interchange format
Name:           protobuf
Version:        2.6.1
Release:        7%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/google/protobuf/
Source0:        protobuf-%{version}.tar.gz
%define         sha1 protobuf=a8f11eced7352edfefa814996ebf086ab3cfbaa0
Patch0:         omit-google-apputils-for-python3.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:	which
BuildRequires:  libstdc++
BuildRequires:  curl
BuildRequires:  make
BuildRequires:  unzip
BuildRequires:  python-dateutil
BuildRequires:  python3-dateutil
BuildRequires:  python-pip

%description
Protocol Buffers (a.k.a., protobuf) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. You can find protobuf's documentation on the Google Developers site.

%package        devel
Summary:        Development files for protobuf
Group:          Development/Libraries
Requires:       protobuf = %{version}-%{release}

%description    devel
The protobuf-devel package contains libraries and header files for
developing applications that use protobuf.

%package        static
Summary:        protobuf static lib
Group:          Development/Libraries
Requires:       protobuf = %{version}-%{release}

%description    static
The protobuf-static package contains static protobuf libraries.

%package        python
Summary:        protobuf python lib
Group:          Development/Libraries
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs
Requires:       protobuf = %{version}-%{release}

%description    python
This contains protobuf python libraries.

%package        python3
Summary:        protobuf python3 lib
Group:          Development/Libraries
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       protobuf = %{version}-%{release}

%description    python3
This contains protobuf python3 libraries.

%package        java
Summary:        protobuf java
Group:          Development/Libraries
BuildRequires:  openjre
BuildRequires:  openjdk
BuildRequires:  apache-maven >= 3.3.3
Requires:       openjre

%description    java
This contains protobuf java package.

%prep
%setup
%patch0 -p1
autoreconf -iv

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
%configure --disable-silent-rules
pip install google-apputils
make %{?_smp_mflags}
pushd python
python setup.py build
python3 setup.py build
popd
pushd java
mvn package
popd

%install
make DESTDIR=%{buildroot} install
pushd python
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
pushd java
mvn install
install -vdm755 %{buildroot}%{_libdir}/java/protobuf
install -vm644 target/protobuf-java-2.6.1.jar %{buildroot}%{_libdir}/java/protobuf
popd

%check
make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/protoc
%{_libdir}/libprotobuf-lite.so.*
%{_libdir}/libprotobuf.so.*
%{_libdir}/libprotoc.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libprotobuf-lite.la
%{_libdir}/libprotobuf-lite.so
%{_libdir}/libprotobuf.la
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.la
%{_libdir}/libprotoc.so

%files static
%defattr(-,root,root)
%{_libdir}/libprotobuf-lite.a
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a

%files python
%{_libdir}/python2.7/site-packages/*

%files python3
%{_libdir}/python3.5/site-packages/*

%files java
%{_libdir}/java/protobuf/*.jar

%changelog
*   Thu May 20 2021 Tapas Kundu <tkundu@vmware.com> 2.6.1-7
-   Removed google-apputils from python3 build.
-   Installed google-apputils in python2 build
*   Fri Nov 08 2019 Tapas Kundu <tkundu@vmware.com> 2.6.1-6
-   Added python-dateutils in BR.
*   Wed Sep 04 2019 Ankit Jain <ankitja@vmware.com> 2.6.1-5
-   Modified the path of JAVA_HOME
*   Fri May 19 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.6.1-4
-   Use JAVA_VERSION macro instead of hard coded version.
*   Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-3
-   Build protobuf python and java.
*   Mon Mar 20 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
-   Build static lib.
*   Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 2.6.1-1
-   Initial packaging for Photon
