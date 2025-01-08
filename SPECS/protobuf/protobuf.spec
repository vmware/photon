%define network_required 1
%define java_min_ver_needed     3.3.3

Summary:        Google's data interchange format
Name:           protobuf
Version:        3.23.3
Release:        3%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/google/protobuf

Source0: https://github.com/protocolbuffers/protobuf/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=d6f360c3d0a205b012c2db6d5c32fc7cde075941e12dd7cb9da8c03ab1f6cb81044acac34b39bb699dde5bea4558159a5e47beafd87e47d6b91d06b37ea6e886

Source1: license.txt
%include %{SOURCE1}

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: libstdc++
BuildRequires: curl
BuildRequires: make
BuildRequires: unzip
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml
BuildRequires: chkconfig
BuildRequires: openjdk11
BuildRequires: apache-maven
BuildRequires: cmake
BuildRequires: gtest-devel
BuildRequires: gmock-devel
BuildRequires: abseil-cpp-devel

Requires: abseil-cpp

%description
Protocol Buffers (a.k.a., %{name}) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data.
You can find %{name}'s documentation on the Google Developers site.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       abseil-cpp-devel

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
rm java/core/src/test/java/com/google/%{name}/IsValidUtf8Test.java \
   java/core/src/test/java/com/google/%{name}/DecodeUtf8Test.java

%build
%{cmake} \
    -Dprotobuf_BUILD_TESTS=OFF \
    -Dprotobuf_ABSL_PROVIDER=package \
    -Dprotobuf_BUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%{cmake_build}

export PROTOC="${PWD}/%{__cmake_builddir}/protoc"

pushd python
%{py3_build}
popd

pushd java
ln -sfrv ${PROTOC} ../
mvn -e -B package \
    -Dhttps.protocols=TLSv1.2 \
    -Dmaven.test.skip=true
popd

%install
%{cmake_install}

export PROTOC="%{_builddir}/%{name}-%{version}/%{__cmake_builddir}/protoc"

pushd python
%{py3_install}
popd

pushd java
mvn -e -B install \
    -Dhttps.protocols=TLSv1.2 \
    -Dmaven.test.skip=true

install -vdm755 %{buildroot}%{_libdir}/java/%{name}

for fn in $(find . -name "*.jar"); do
  install -vm644 ${fn} %{buildroot}%{_libdir}/java/%{name}
done
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/protoc*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/cmake/*

%files static
%defattr(-,root,root)

%files python3
%defattr(-,root,root)
%{python3_sitelib}/*

%files java
%defattr(-,root,root)
%{_libdir}/java/protobuf/*.jar

%changelog
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.23.3-3
- Release bump for network_required packages
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.23.3-2
- Release bump for SRP compliance
* Tue Nov 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.23.3-1
- Upgrade to v3.23.3
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.21.12-3
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.21.12-2
- Bump version as a part of openjdk11 upgrade
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.21.12-1
- Upgrade to v3.21.2
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
