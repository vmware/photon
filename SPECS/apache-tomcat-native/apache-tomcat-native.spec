Summary:        Apache Tomcat Native
Name:           apache-tomcat-native
Version:        2.0.3
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://tomcat.apache.org/native-doc/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64
Source0:        https://dlcdn.apache.org/tomcat/tomcat-connectors/native/%{version}/source/tomcat-native-%{version}-src.tar.gz
%define sha512  tomcat-native=d80e6b76295bb253eaf6eab4d722f3ba2f683f33a96310838b4c44b99f0b47a49ed9c09bb53ed23698db057ce765e3fcbfcd4ac4b75d2bdbe691f916be3be339
Patch0:         openssl_3_0_7_compatibility.patch
BuildRequires:  openjdk11
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  apr-devel
Requires:       apr
Requires:       openssl

%description
The Apache Tomcat Native Library is an optional component for use with Apache Tomcat
that allows Tomcat to use certain native resources for performance, compatibility, etc.

%package        devel
Summary:        Apache Tomcat Native development package
Requires:       %{name} = %{version}-%{release}

%description    devel
Apache Tomcat Native development package

%prep
%autosetup -p1 -n tomcat-native-%{version}-src

%build
export JAVA_HOME=/usr/lib/jvm/OpenJDK-1.11.0
cd native
%configure --with-apr=%{_prefix} \
           --with-java-home=$JAVA_HOME \
           --with-ssl=%{_prefix}

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
%{_libdir}/libtcnative*.so.0.*
%exclude %{_libdir}/libtcnative-2.a

%files devel
%defattr(-,root,root,-)
%{_libdir}/libtcnative*.so
%{_libdir}/libtcnative*.so.0

%changelog
* Fri Mar 03 2023 Srish Srinivasan <ssrish@vmware.com> 2.0.3-1
- Update to v2.0.3
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 1.2.24-4
- Use openjdk11
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.24-3
- Bump up release for openssl
* Thu Sep 10 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.24-2
- Openssl 1.1.1 compatibility
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 1.2.24-1
- Initial build.  First version
