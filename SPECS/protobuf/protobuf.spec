%define java_min_ver_needed     1.8.0.45

Summary:        Google's data interchange format
Name:           protobuf
Version:        3.19.6
Release:        5%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/google/protobuf

Source0: https://github.com/protocolbuffers/protobuf/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=8f92242f2be8e1bbfba41341c87709ad91ad83b8b3e3df88bb430411541d3399295f49291fd52b50e3487b0fce33181cb4d175685fd25aac72adfaee26a612d4

BuildRequires:  build-essential
BuildRequires:  curl
BuildRequires:  unzip
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  chkconfig
BuildRequires:  openjdk8
BuildRequires:  apache-maven

%description
Protocol Buffers (a.k.a., protobuf) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data.
You can find protobuf's documentation on the Google Developers site.

%package        devel
Summary:        Development files for protobuf
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The protobuf-devel package contains libraries and header files for
developing applications that use protobuf.

%package        static
Summary:        protobuf static lib
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    static
The protobuf-static package contains static protobuf libraries.

%package        python3
Summary:        protobuf python3 lib
Group:          Development/Libraries
Requires:       python3
Requires:       %{name} = %{version}-%{release}

%description    python3
This contains protobuf python3 libraries.

%package        java
Summary:        protobuf java
Group:          Development/Libraries
Requires:       (openjre8 >= %{java_min_ver_needed} or openjdk11-jre or openjdk17-jre)

%description    java
This contains protobuf java package.

%prep
%autosetup -p1

# This test is incredibly slow on arm
# https://github.com/google/protobuf/issues/2389
%if "%{_arch}" == "aarch64"
rm -f java/core/src/test/java/com/google/%{name}/IsValidUtf8Test.java \
      java/core/src/test/java/com/google/%{name}/DecodeUtf8Test.java
%endif

autoreconf -vfi

%build
%configure \
    --disable-silent-rules \
    --disable-static

%make_build

pushd python
%{py3_build}
popd

pushd java
mvn package
popd

%install
%make_install %{?_smp_mflags}

pushd python
%{py3_install}
popd

pushd java
mvn install
install -vdm755 %{buildroot}%{_libdir}/java/%{name}
install -vm644 core/target/%{name}-java-%{version}.jar %{buildroot}%{_libdir}/java/%{name}
install -vm644 util/target/%{name}-java-util-%{version}.jar %{buildroot}%{_libdir}/java/%{name}
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/protoc
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so

%files static
%defattr(-,root,root)

%files python3
%defattr(-,root,root)
%{python3_sitelib}/*

%files java
%defattr(-,root,root)
%{_libdir}/java/%{name}/*.jar

%changelog
* Fri Jun 07 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.19.6-5
- Fix requires of protobuf
- jre is needed by protobuf-java, not protobuf
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.19.6-4
- Bump version as a part of openjdk8 upgrade
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.19.6-3
- Require jre8 or jdk11-jre or jdk17-jre
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.19.6-2
- Bump version as a part of openjdk8 upgrade
* Wed Jun 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.19.6-1
- Upgrade to v3.19.6
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.19.4-2
- Remove .la files
* Wed Mar 02 2022 Harinadh D <hdommaraju@vmware.com> 3.19.4-1
- Version update
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.14.0-2
- Bump up to compile with python 3.10
* Wed Feb 10 2021 Harinadh D <hdommaraju@vmware.com> 3.14.0-1
- Update protobuf
* Fri Oct 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.13.0-2
- Disabled few slow tests on aarch64
* Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 3.13.0-1
- Automatic Version Bump
* Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.12.3-1
- Automatic Version Bump
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 3.6.1-2
- Mass removal python2
* Tue Sep 18 2018 Tapas Kundu <tkundu@vmware.com> 3.6.1-1
- Update to version 3.6.1
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-6
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.2.0-5
- Use python2 explicitly while building
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.2.0-4
- Renamed openjdk to openjdk8
* Fri Apr 28 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.0-3
- Update python3 version
* Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.2.0-2
- Build protobuf-java.
* Fri Mar 31 2017 Rongrong Qiu <rqiu@vmware.com> 3.2.0-1
- Upgrade to 3.2.0
* Tue Mar 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-3
- Build protobuf-python.
* Mon Mar 20 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
- Build static lib.
* Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 2.6.1-1
- Initial packaging for Photon
