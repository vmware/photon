Summary:        Apache Tomcat Native
Name:           apache-tomcat-native
Version:        1.2.24
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://tomcat.apache.org/native-doc/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64
Source0:        http://apachemirror.wuchna.com/tomcat/tomcat-connectors/native/%{version}/source/tomcat-native-%{version}-src.tar.gz
%define sha1    tomcat-native=eb278be30134136204a9d417a25b2536c0160666
BuildRequires:  openjdk8
BuildRequires:  openssl-devel
BuildRequires:  apr-devel
Requires:       apr
Requires:       openssl

%description
The Apache Tomcat Native Library is an optional component for use with Apache Tomcat
that allows Tomcat to use certain native resources for performance, compatibility, etc.

%prep
%setup -q -n tomcat-native-%{version}-src

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
cd native
%configure --with-apr=%{_prefix} \
           --with-java-home=/usr/lib/jvm/OpenJDK-1.8.0/ \
           --with-ssl=yes

make %{?_smp_mflags}

%install
cd native
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libtcnative-1.so
%{_libdir}/libtcnative-1.so.0
%{_libdir}/libtcnative-1.so.0.2.24
%exclude %{_libdir}/libtcnative-1.a
%exclude %{_libdir}/libtcnative-1.la

%changelog
*   Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 1.2.24-1
-   Initial build.  First version
