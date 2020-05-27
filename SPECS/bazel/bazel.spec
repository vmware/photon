%global debug_package %{nil}
%define __os_install_post %{nil}

Summary:        Build software of any size, quickly and reliably, just as engineers do at Google.
Name:           bazel
Version:        2.0.0
Release:        2%{?dist}
License:        Apache License 2.0
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://bazel.build/
Source:         https://github.com/bazelbuild/bazel/releases/download/%{version}/%{name}-%{version}.dist.zip
%define sha1    bazel=f4e2eca5ff6c1c1cb921ea6637c1ec758ba93128
BuildRequires:  openjdk8 zlib-devel which findutils tar gzip zip unzip
BuildRequires:  gcc
BuildRequires:  python3
Requires:       openjdk8

%description
Bazel is Google's own build tool, now publicly available in Beta. Bazel has
built-in support for building both client and server software, including client
applications for both Android and iOS platforms. It also provides an extensible
framework that you can use to develop your own build rules.

%prep
%setup  -c -n %{name}-%{version}

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
mkdir /usr/tmp
export TMPDIR=/usr/tmp
# some modules in bazel just expecting python to be exist
ln -sf %{_bindir}/python3 %{_bindir}/python
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
* Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 2.0.0-2
- Changed openjdk install directory name
* Fri Feb 7 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 2.0.0-1
- Initial release

