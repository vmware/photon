Summary:        Apache Tomcat Native
Name:           apache-tomcat-native
Version:        1.2.24
Release:        4%{?dist}
License:        Apache 2.0
URL:            https://tomcat.apache.org/native-doc/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64
Source0:        http://apachemirror.wuchna.com/tomcat/tomcat-connectors/native/%{version}/source/tomcat-native-%{version}-src.tar.gz
%define sha512  tomcat-native=5dae151a60f8bd5a9a29d63eca838c77174426025ee65a826f0698943494dd3656d50bcd417e220a926b9ce111ea167043d4b806264030e951873d06767b3d6f
Patch0:         openssl_1_1_1_compatibility.patch
BuildRequires:  openjdk11
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  apr-devel
Requires:       apr
Requires:       openssl

%description
The Apache Tomcat Native Library is an optional component for use with Apache Tomcat
that allows Tomcat to use certain native resources for performance, compatibility, etc.

%prep
%autosetup -p1 -n tomcat-native-%{version}-src

%build
export JAVA_HOME=/usr/lib/jvm/OpenJDK-1.11.0
cd native
%configure --with-apr=%{_prefix} \
           --with-java-home=$JAVA_HOME \
           --with-ssl=yes

make %{?_smp_mflags}

%install
cd native
make DESTDIR=%{buildroot} install %{?_smp_mflags}

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
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 1.2.24-4
- Use openjdk11
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.24-3
- Bump up release for openssl
* Thu Sep 10 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.24-2
- Openssl 1.1.1 compatibility
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 1.2.24-1
- Initial build.  First version
