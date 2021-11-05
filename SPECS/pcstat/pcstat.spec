Summary:        A tool that inspect which pages of a file or files are being cached by the Linux kernel
Name:           pcstat
Version:        1
Release:        15%{?dist}
License:        Apache
URL:            https://github.com/tobert/pcstat
Group:          Development/Debuggers
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/tobert/pcstat/archive/pcstat-1.zip
%define sha1    pcstat=cd67c42d291763597dbe3fb19e8e367c54a4a898
Source1:        https://github.com/golang/sys/golang-sys-08-02-2017.zip
%define sha1    golang-sys=7f713451011d127755448c6603c15dc907bc47bc
Patch0:         pcstat-aarch64-support.patch
BuildRequires:  unzip go audit git
Requires:       go
%description
A tool that inspect which pages of a file or files are being cached by the Linux kernel

%prep
%autosetup -p1 -n %{name}-master

%build
cd ..
unzip %{SOURCE1}
mkdir -p build/src/github.com/tobert/pcstat
mkdir -p build/src/golang.org/x/sys
mkdir -p build/bin
cp -r %{name}-master/* build/src/github.com/tobert/%{name}/.
cp -r sys-master/* build/src/golang.org/x/sys
cd build
export GOPATH=`pwd`
export GO111MODULE=auto
cd bin
export GOBIN=`pwd`
export PATH=$PATH:$GOBIN
cd ../src/github.com/tobert/%{name}
go build
cd %{name}
go build
go install

%install
mkdir -p %{buildroot}/%{_bindir}
cp ../build/bin/pcstat %{buildroot}/%{_bindir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/pcstat

%changelog
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1-15
-   Bump up version to compile with new go
*   Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1-14
-   Bump up version to compile with new go
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1-13
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1-12
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1-11
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1-10
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1-9
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1-8
-   Bump up version to compile with go 1.13.3
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1-7
-   Bump up version to compile with new go
*   Wed Jan 03 2018 Alexey Makhalov <amakhalov@vmware.com> 1-6
-   Aarch64 support
*   Wed Aug 02 2017 Dheeraj Shetty <dheerajs@vmware.com> 1-5
-   Remove the build time dependencies and avoid downloading from github
*   Tue Mar 07 2017 XIaolin Li <xiaolinl@vmware.com> 1-4
-   Moved executable from /usr/local/bin to /usr/bin.
*   Fri Feb 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1-3
-   Fix the build.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1-2
-   GA - Bump release of all rpms
*   Wed Nov 25 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.7.3-1
-   Initial build.  First version
