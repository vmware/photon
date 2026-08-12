%define srcname tomcat-native

Summary:        Apache Tomcat Native
Name:           apache-tomcat-native
Version:        1.3.8
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://tomcat.apache.org/native-doc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64

Source0: https://archive.apache.org/dist/tomcat/tomcat-connectors/native/%{version}/source/%{srcname}-%{version}-src.tar.gz
%define sha512 %{srcname}=a12b97979037720465300cbc05777ff6ee2ec1dc59ff698864d7068800bf0c2d2606a4e0e29a4d7b16f92c9130604a13e0cc27929a224c9ff77e532ac98a4695

BuildRequires:  openjdk8
BuildRequires:  openssl-devel
BuildRequires:  apr-devel

Requires:       apr
Requires:       openssl
Requires:       (openjre8 or openjdk11-jre or openjdk17-jre or openjdk21-jre)
Conflicts:      apache-tomcat < 9.0.0

%description
The Apache Tomcat Native Library is an optional component for use with Apache Tomcat
that allows Tomcat to use certain native resources for performance, compatibility, etc.

%prep
%autosetup -n %{srcname}-%{version}-src

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
%{_libdir}/libtcnative-1.so.0.3.8
%exclude %{_libdir}/libtcnative-1.a

%changelog
* Wed Aug 12 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.3.8-1
- Upgrade to 1.3.8, drop openssl_1_1_1_compatibility.patch (no longer needed; upstream now supports OpenSSL >= 1.1.1 natively)
* Sat Aug 23 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.24-7
- Add jdk21 to requires list
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
