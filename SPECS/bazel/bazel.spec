%global debug_package %{nil}
%define __os_install_post %{nil}

Summary:        Build software of any size, quickly and reliably, just as engineers do at Google.
Name:           bazel
Version:        5.3.0
Release:        1%{?dist}
License:        Apache License 2.0
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://bazel.build/
Source:         https://github.com/bazelbuild/bazel/releases/download/%{version}/%{name}-%{version}-dist.zip
%define sha512  bazel=6c98e904596764a309e98ea2453c751dc0bf27c683462c5654b72076f8537bccf6c5103ccea60fa3a3dffeaa76b07db80a594feb96ed566282d10bb04f0e1455
BuildRequires:  openjdk11 zlib-devel which findutils tar gzip zip unzip
BuildRequires:  gcc
BuildRequires:  python3
Requires:       openjdk11

%description
Bazel is Google's own build tool, now publicly available in Beta. Bazel has
built-in support for building both client and server software, including client
applications for both Android and iOS platforms. It also provides an extensible
framework that you can use to develop your own build rules.

%prep
%autosetup -c -n %{name}-%{version}

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
mkdir /usr/tmp
export TMPDIR=/usr/tmp
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
