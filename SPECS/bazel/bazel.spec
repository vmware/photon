%define network_required 1
%global debug_package %{nil}
%define __os_install_post %{nil}

Summary:        Build software of any size, quickly and reliably, just as engineers do at Google.
Name:           bazel
Version:        5.3.2
Release:        4%{?dist}
License:        Apache License 2.0
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://bazel.build/

Source0: https://github.com/bazelbuild/bazel/releases/download/%{version}/%{name}-%{version}-dist.zip
%define sha512 %{name}=a63895c224d51619cf83e6e55872aa6d55d17c7dcea59eaf467069d2c95259f5964fbf8fa5994df0e3c030234a7adf70a2715edb4edbbe2bf69d21dd698c0833

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

Requires: (openjdk11 or openjdk17)

%description
Bazel is Google's own build tool, now publicly available in Beta. Bazel has
built-in support for building both client and server software, including client
applications for both Android and iOS platforms. It also provides an extensible
framework that you can use to develop your own build rules.

%prep
%autosetup -p1 -c -n %{name}-%{version}

%build
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)
export TMPDIR=%{_usr}/tmp

mkdir $TMPDIR

./compile.sh

pushd output
./bazel
popd

%install
mkdir -p %{buildroot}%{_bindir}
cp output/bazel %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/bazel

%changelog
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.2-4
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.2-3
- Bump version as a part of openjdk11 upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.3.2-2
- Update release to compile with python 3.11
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 5.3.2-1
- Automatic Version Bump
* Sun Sep 18 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.3.0-1
- Upgrade to latest version
- Use openjdk11
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 4.0.0-1
- Automatic Version Bump
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 3.5.0-2
- GCC-10 support.
* Mon Sep 21 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 3.5.0-1
- Update bazel version
* Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 2.0.0-2
- Changed openjdk install directory name
* Fri Feb 7 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 2.0.0-1
- Initial release
