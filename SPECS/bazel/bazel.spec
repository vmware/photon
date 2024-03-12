%global debug_package %{nil}
%define __os_install_post %{nil}

Summary:        Build software of any size, quickly and reliably, just as engineers do at Google.
Name:           bazel
Version:        6.1.2
Release:        4%{?dist}
License:        Apache License 2.0
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://bazel.build

Source0: https://github.com/bazelbuild/bazel/releases/download/%{version}/%{name}-%{version}-dist.zip
%define sha512 %{name}=3b84139d383f47607db92f3f59504b2e07409140ebfad7d540a81638619ba67eb870285c9b9c6db8dd50a8971ba871365d583bdf9754ff0038d5b6c39af9d013

BuildRequires:  openjdk11
BuildRequires:  zlib-devel
BuildRequires:  which
BuildRequires:  findutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  zip
BuildRequires:  unzip
BuildRequires:  gcc
BuildRequires:  python3

Requires:   (openjdk11 or openjdk17)

%description
Bazel is Google's own build tool, now publicly available in Beta. Bazel has
built-in support for building both client and server software, including client
applications for both Android and iOS platforms. It also provides an extensible
framework that you can use to develop your own build rules.

%prep
%autosetup -p1 -c

%build
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK-*)
mkdir -p /usr/tmp
export TMPDIR=/usr/tmp
./compile.sh
pushd output
./bazel
popd

%install
mkdir -p %{buildroot}%{_bindir}
cp output/bazel %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/bazel

%changelog
* Mon Mar 11 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 6.1.2-4
- Version bump to use new jdk11
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.2-3
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.2-2
- Bump version as a part of openjdk11 upgrade
* Tue May 09 2023 Harinadh D <hdommaraju@vmware.com> 6.1.2-1
- Version upgrade
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.5.0-3
- Bump up to compile with python 3.10
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 3.5.0-2
- GCC-10 support.
* Mon Sep 21 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 3.5.0-1
- Update bazel version
* Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 2.0.0-2
- Changed openjdk install directory name
* Fri Feb 7 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 2.0.0-1
- Initial release
