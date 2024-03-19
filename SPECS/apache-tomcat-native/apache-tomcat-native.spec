%define srcname tomcat-native

Summary:        Apache Tomcat Native
Name:           apache-tomcat-native
Version:        1.2.24
Release:        6%{?dist}
License:        Apache 2.0
URL:            https://tomcat.apache.org/native-doc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64

Source0: http://apachemirror.wuchna.com/tomcat/tomcat-connectors/native/%{version}/source/%{srcname}-%{version}-src.tar.gz
%define sha512 %{srcname}=5dae151a60f8bd5a9a29d63eca838c77174426025ee65a826f0698943494dd3656d50bcd417e220a926b9ce111ea167043d4b806264030e951873d06767b3d6f

Patch0:         openssl_1_1_1_compatibility.patch

BuildRequires:  openjdk8
BuildRequires:  openssl-devel
BuildRequires:  apr-devel

Requires:       apr
Requires:       openssl
Requires:       (openjre8 or openjdk11-jre or openjdk17-jre)

%description
The Apache Tomcat Native Library is an optional component for use with Apache Tomcat
that allows Tomcat to use certain native resources for performance, compatibility, etc.

%prep
%autosetup -p1 -n %{srcname}-%{version}-src

%build
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK*)

cd native
%configure \
    --with-apr=%{_prefix} \
    --with-java-home=$JAVA_HOME/ \
    --with-ssl=yes

%make_build

%install
cd native
%make_install %{?_smp_mflags}

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

%changelog
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.2.24-6
- Bump version as a part of openjdk8 upgrade
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.24-5
- Require jre8 or jdk11-jre or jdk17-jre
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.24-4
- Bump version as a part of openjdk8 upgrade
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.24-3
- Bump up release for openssl
* Thu Sep 10 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.24-2
- Openssl 1.1.1 compatibility
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 1.2.24-1
- Initial build.  First version
