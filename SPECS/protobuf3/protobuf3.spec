Summary:        Google's data interchange format
Name:           protobuf3
Version:        3.0.0
Release:        4%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/google/protobuf/
Source0:        protobuf-%{version}.tar.gz
%define         sha1 protobuf=cffdb9bd6eed66b7c3322197740510fd103bb6df
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  libtool
BuildRequires:	which
BuildRequires:  libstdc++
BuildRequires:  curl
BuildRequires:  make
BuildRequires:  unzip
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python-setuptools
BuildRequires:  chkconfig
BuildRequires:  openjre
BuildRequires:  openjdk
BuildRequires:  apache-maven >= 3.3.3
Provides:       protobuf
Conflicts:      protobuf < %{version}
Obsoletes:      protobuf < %{version}

%description
Protocol Buffers (a.k.a., protobuf) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. You can find protobuf's documentation on the Google Developers site.

%package        devel
Summary:        Development files for protobuf
Group:          Development/Libraries
Requires:       protobuf3 = %{version}-%{release}
Provides:       protobuf-devel
Conflicts:      protobuf-devel < %{version}
Obsoletes:      protobuf-devel < %{version}

%description    devel
The protobuf-devel package contains libraries and header files for
developing applications that use protobuf.

%package        static
Summary:        protobuf3 static lib
Group:          Development/Libraries
Requires:       protobuf3 = %{version}-%{release}
Provides:       protobuf-static
Conflicts:      protobuf-static < %{version}
Obsoletes:      protobuf-static < %{version}

%description    static
The protobuf-static package contains static protobuf libraries.

%package        python
Summary:        protobuf3 python lib
Group:          Development/Libraries
Requires:       python2
Requires:       python2-libs
Requires:       protobuf3 = %{version}-%{release}
Provides:       protobuf-python
Conflicts:      protobuf-python < %{version}
Obsoletes:      protobuf-python < %{version}

%description    python
This contains protobuf python libraries.

%package        python3
Summary:        protobuf3 python3 lib
Group:          Development/Libraries
Requires:       python3
Requires:       python3-libs
Requires:       protobuf3 = %{version}-%{release}
Provides:       protobuf-python3
Conflicts:      protobuf-python3 < %{version}
Obsoletes:      protobuf-python3 < %{version}

%description    python3
This contains protobuf python3 libraries.

%package        java
Summary:        protobuf3 java
Group:          Development/Libraries
Requires:       openjre
Provides:       protobuf-java
Conflicts:      protobuf-java < %{version}
Obsoletes:      protobuf-java < %{version}

%description    java
This contains protobuf java package.

%prep
%setup -n protobuf-%{version}
autoreconf -iv

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
%configure --disable-silent-rules
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
install -vm644 core/target/protobuf-java-%{version}.jar %{buildroot}%{_libdir}/java/protobuf
install -vm644 util/target/protobuf-java-util-%{version}.jar %{buildroot}%{_libdir}/java/protobuf
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
*   Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 3.0.0-4
-   Moved BuildRequires from sub packages to top
*   Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-3
-   Add conflicts.
*   Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-2
-   Add provides, remove debug printenv.
*   Tue Jun 27 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-1
-   protobuf v3.0.0
