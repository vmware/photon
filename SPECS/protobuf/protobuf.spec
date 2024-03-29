%define java_min_ver_needed     3.3.3

Summary:        Google's data interchange format
Name:           protobuf
Version:        3.21.12
Release:        3%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/google/protobuf

Source0: https://github.com/protocolbuffers/protobuf/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=152f8441c325e808b942153c15e82fdb533d5273b50c25c28916ec568ada880f79242bb61ee332ac5fb0d20f21239ed6f8de02ef6256cc574b1fc354d002c6b0

BuildRequires: build-essential
BuildRequires: curl
BuildRequires: unzip
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml
BuildRequires: chkconfig
BuildRequires: openjdk11
BuildRequires: apache-maven >= %{java_min_ver_needed}

%description
Protocol Buffers (a.k.a., %{name}) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data.
You can find %{name}'s documentation on the Google Developers site.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        static
Summary:        %{name} static lib
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    static
The %{name}-static package contains static %{name} libraries.

%package        python3
Summary:        %{name} python3 lib
Group:          Development/Libraries
Requires:       python3
Requires:       %{name} = %{version}-%{release}

%description    python3
This contains %{name} python3 libraries.

%package        java
Summary:        %{name} java
Group:          Development/Libraries
Requires:       (openjdk11-jre or openjdk17-jre)

%description    java
This contains %{name} java package.

%prep
%autosetup -p1

# This test is incredibly slow
# https://github.com/google/protobuf/issues/2389
rm -f java/core/src/test/java/com/google/%{name}/IsValidUtf8Test.java \
      java/core/src/test/java/com/google/%{name}/DecodeUtf8Test.java

%build
autoreconf -fvi

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

%clean
rm -rf %{buildroot}/*

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
%{_libdir}/java/protobuf/*.jar

%changelog
* Sun Aug 27 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.21.12-3
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.21.12-2
- Bump version as a part of openjdk11 upgrade
* Fri Jun 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.21.12-1
- Upgrade to v21.12
* Fri Mar 03 2023 Srish Srinivasan <ssrish@vmware.com> 3.14.0-5
- bump release as part of apache-maven update
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.14.0-4
- Update release to compile with python 3.11
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 3.14.0-3
- Use openjdk11
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.14.0-2
- Remove .la files
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
