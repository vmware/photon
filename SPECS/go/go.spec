
%global goroot          /usr/lib/golang
%global gopath          %{_datadir}/gocode
%global gohostarch      amd64

# rpmbuild magic to keep from having meta dependency on libc.so.6
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}

Summary:	Go 
Name:		go
Version:	1.4.2
Release:	5%{?dist}
License:	BSD
URL:		https://golang/org
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://storage.googleapis.com/golang/%{name}%{version}.src.tar.gz
%define sha1 go=460caac03379f746c473814a65223397e9c9a2f6
BuildRequires:	mercurial
Requires:	mercurial
# We strip meta dependency, but go requires glibc.
Requires:	glibc

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.  

%prep
%setup -qn %{name}

%build
export GOROOT_FINAL=%{goroot}
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
pushd src
./make.bash --no-clean
popd

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{goroot}

cp -apv api bin doc favicon.ico include lib pkg robots.txt src misc VERSION \
   %{buildroot}%{goroot}

# remove the unnecessary zoneinfo file (Go will always use the system one first)
rm -rfv %{buildroot}%{goroot}/lib/time

# remove the doc Makefile
rm -rfv %{buildroot}%{goroot}/doc/Makefile

# put binaries to bindir, linked to the arch we're building,
# leave the arch independent pieces in %{goroot}
mkdir -p %{buildroot}%{goroot}/bin/linux_%{gohostarch}
mv %{buildroot}%{goroot}/bin/go %{buildroot}%{goroot}/bin/linux_%{gohostarch}/go
mv %{buildroot}%{goroot}/bin/gofmt %{buildroot}%{goroot}/bin/linux_%{gohostarch}/gofmt

# ensure these exist and are owned
mkdir -p %{buildroot}%{gopath}/src/github.com/
mkdir -p %{buildroot}%{gopath}/src/bitbucket.org/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/p/


ln -sfv ../../%{goroot}/bin/linux_%{gohostarch}/gofmt %{buildroot}%{_bindir}/gofmt
ln -sfv ../../%{goroot}/bin/linux_%{gohostarch}/go %{buildroot}%{_bindir}/go

install -vdm644 %{buildroot}/etc/profile.d
cat >> %{buildroot}/etc/profile.d/go-exports.sh <<- "EOF"
export GOROOT=%{goroot}
export GOPATH=%{_datadir}/gocode
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOOS=linux
EOF
chown -R root:root %{buildroot}/etc/profile.d/go-exports.sh


%{_fixperms} %{buildroot}/*

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  #This is uninstall
  rm /etc/profile.d/go-exports.sh
  rm -rf /opt/%{name}
  exit 0
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%exclude %{goroot}/src/*.rc
%exclude %{goroot}/include/plan9
/etc/profile.d/go-exports.sh
%{goroot}/*
%dir %{gopath}
%dir %{gopath}/src
%dir %{gopath}/src/github.com/
%dir %{gopath}/src/bitbucket.org/
%dir %{gopath}/src/code.google.com/
%dir %{gopath}/src/code.google.com/p/
%exclude %{goroot}/src/pkg/debug/dwarf/testdata
%exclude %{goroot}/src/pkg/debug/elf/testdata
%{_bindir}/*

%changelog
*	Thu Jun 2 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.2-5
-	Fix script syntax 
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.2-4
-	GA - Bump release of all rpms
*       Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4.2-3
-       Handling upgrade scenario pre/post/un scripts.
*	Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.4.2-2
-	Edit post script.
*	Mon Aug 03 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.4.2-1
-	Update to golang release version 1.4.2
*	Fri Oct 17 2014 Divya Thaluru <dthaluru@vmware.com> 1.3.3-1
-	Initial build.	First version
