#Do not strip or try to separate debug information
%global debug_package %{nil}
%define __os_install_post %{nil}

# goroot for Photon
%global goroot          %{_libdir}/golang

# rpmbuild magic to keep from having meta dependency on libc.so.6
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}

%ifarch x86_64
%global gohostarch amd64
%endif
%ifarch aarch64
%global gohostarch  arm64
%endif

%ifarch x86_64
%global race 1
%else
%global race 0
%endif

Summary:        Go 
Name:           go
Version:        1.8.1
Release:        3%{?dist}
License:        BSD
URL:            https://golang.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
#The bootstrap go1.4, see https://golang.org/doc/install/source#go14
Source0:	https://storage.googleapis.com/golang/go1.4-bootstrap-20170531.tar.gz
%define sha1    go1.4-bootstrap=30e8507eb0c984a1f53aa6a006882cf45235e148
Source1:        https://storage.googleapis.com/golang/%{name}%{version}.src.tar.gz
%define sha1    go%{version}.src.tar.gz=0c4b7116bd6b7cdc19bdcf8336c75eae4620907b
Requires:       glibc

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.  

%prep
%setup -q -c -n bootstrap
mkdir ../go
%setup -q -D -T -b 1 -n go

%build
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}

pushd ../bootstrap/go/src
# Now in the old go toolchain for bootstrapping
# Disable cgo, as Go1.4 has problem with it
# It doesn't affect the bootstrapping of the new toolchain
CGO_ENABLED=0 ./make.bash
popd

# Now in the new go toolchain
pushd src
export GOROOT_FINAL=%{goroot}
GOROOT_BOOTSTRAP="$(pwd)/../../bootstrap/go" ./make.bash --no-clean
popd

%if %{race}
GOROOT="$(pwd)" PATH="$(pwd)/bin:$PATH" go install -race std
%endif

%check
export GOROOT=$(pwd -P)
export PATH="$GOROOT"/bin:"$PATH"
cd src
./run.bash --no-rebuild -v -v -v -k

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{goroot}

cp -R api bin doc favicon.ico lib pkg robots.txt src misc test VERSION %{buildroot}%{goroot}

# put binaries to bindir, linked to the arch we're building,
# leave the arch independent pieces in %{goroot}
mkdir -p %{buildroot}%{goroot}/bin/linux_%{gohostarch}
mv %{buildroot}%{goroot}/bin/go %{buildroot}%{goroot}/bin/linux_%{gohostarch}/go
mv %{buildroot}%{goroot}/bin/gofmt %{buildroot}%{goroot}/bin/linux_%{gohostarch}/gofmt

ln -snrfv %{buildroot}%{goroot}/bin/linux_%{gohostarch}/go %{buildroot}%{goroot}/bin/go
ln -snrfv %{buildroot}%{goroot}/bin/linux_%{gohostarch}/gofmt %{buildroot}%{goroot}/bin/gofmt

ln -snfv %{goroot}/bin/linux_%{gohostarch}/gofmt %{buildroot}%{_bindir}/gofmt
ln -snfv %{goroot}/bin/linux_%{gohostarch}/go %{buildroot}%{_bindir}/go

%{_fixperms} %{buildroot}/*

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc AUTHORS CONTRIBUTORS LICENSE PATENTS
%doc %{goroot}/VERSION
%dir %{goroot}/doc
%doc %{goroot}/doc/*
%{goroot}/favicon.ico
%{goroot}/robots.txt
%{goroot}/api
%{goroot}/bin
%{goroot}/lib
%{goroot}/pkg
%{goroot}/src
%{goroot}/misc
%{goroot}/test
%{_bindir}/*

%changelog
*   Mon Oct 02 2017 Bo Gan <ganb@vmware.com> 1.8.1-3
-   Clean up spec, remove env variables and add arm64 support
*   Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-2
-   Remove mercurial from buildrequires and requires.
*   Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> 1.8.1-1
-   Update Golang to version 1.8.1, updated patch0
*   Wed Dec 28 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.4-1
-   Updated Golang to 1.7.4.
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.6.3-2
-   Modified %check
*   Wed Jul 27 2016 Anish Swaminathan <anishs@vmware.com> 1.6.3-1
-   Update Golang to version 1.6.3 - fixes CVE 2016-5386
*   Fri Jul 8 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.6.2-1
-   Updated the Golang to version 1.6.2
*   Thu Jun 2 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.2-5
-   Fix script syntax 
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.2-4
-   GA - Bump release of all rpms
*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4.2-3
-   Handling upgrade scenario pre/post/un scripts.
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.4.2-2
-   Edit post script.
*   Mon Aug 03 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.4.2-1
-   Update to golang release version 1.4.2
*   Fri Oct 17 2014 Divya Thaluru <dthaluru@vmware.com> 1.3.3-1
-   Initial build.  First version
