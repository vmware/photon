%global debug_package %{nil}
%define __os_install_post %{nil}

Summary:        Build software of any size, quickly and reliably, just as engineers do at Google.
Name:           bazel
Version:        2.0.0
Release:        1%{?dist}
License:        Apache License 2.0
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://bazel.build/
Source:         https://github.com/bazelbuild/bazel/releases/download/%{version}/%{name}-%{version}.dist.zip
%define sha1    bazel=f4e2eca5ff6c1c1cb921ea6637c1ec758ba93128
Requires:       openjdk8
BuildRequires:  openjdk8 zlib-devel which findutils tar gzip zip unzip
BuildRequires:  gcc
BuildRequires:  python3

%description
Bazel is Google's own build tool, now publicly available in Beta. Bazel has
built-in support for building both client and server software, including client
applications for both Android and iOS platforms. It also provides an extensible
framework that you can use to develop your own build rules.

%prep
%setup -c -n %{name}-%{version}

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
mkdir /usr/tmp
export TMPDIR=/usr/tmp
# some modules in bazel just expecting python to be exist
ln -sf %{_bindir}/python3 %{_bindir}/python
env ./compile.sh
env ./output/bazel
env ./output/bazel shutdown

%install
mkdir -p %{buildroot}%{_bindir}
cp output/bazel %{buildroot}%{_bindir}


%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/bazel

%changelog
*	Fri Apr 10 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 2.0.0-1
-	Update bazel to v2.0.0
*	Wed Apr 01 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 0.24.1-2
-	Cleanup bazel server after build
*	Thu May 9 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 0.24.1-1
-	Add bazel package to photon2.0 to build envopy-1.10.0
*	Thu Apr 04 2019 Tapas Kundu <tkundu@vmware.com> 0.24.1-1
-	Initial packaging for bazel in Photon.

