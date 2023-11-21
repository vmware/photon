Summary:        A tool that inspect which pages of a file or files are being cached by the Linux kernel
Name:           pcstat
Version:        1
Release:        19%{?dist}
License:        Apache
URL:            https://github.com/tobert/%{name}
Group:          Development/Debuggers
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/tobert/%{name}/archive/%{name}-1.zip
%define sha512  %{name}=7f62d16447fe5f8e9c126fb4f0e00df697bb253ea0213ece2be2ce0b919ccaa175e009987a4f01252225c35b05c55685da4db684d68b7bd4501fe781163d01d3
Source1:        https://github.com/golang/sys/golang-sys-08-02-2017.zip
%define sha512  golang-sys=0c40f2acd0466637b5b01f75eed593939075fc742c8991b4ff884076852a5c02eb6ed0a162be8539ff73eba665ae04fb011efe739c4bda999f5365241945015a
Patch0:         %{name}-aarch64-support.patch
BuildRequires:  unzip go audit git
Requires:       go
%description
A tool that inspect which pages of a file or files are being cached by the Linux kernel

%prep
%autosetup -p1 -n %{name}-master

%build
cd ..
unzip %{SOURCE1}
mkdir -p build/src/github.com/tobert/%{name}
mkdir -p build/src/golang.org/x/sys
mkdir -p build/bin
cp -r %{name}-master/* build/src/github.com/tobert/%{name}/.
cp -r sys-master/* build/src/golang.org/x/sys
cd build
export GOPATH=`pwd`
cd bin
export GOBIN=`pwd`
export PATH=$PATH:$GOBIN
cd ../src/github.com/tobert/%{name}
export GO111MODULE=auto
go build
cd %{name}
go build
go install

%install
mkdir -p %{buildroot}/%{_bindir}
cp ../build/bin/%{name} %{buildroot}/%{_bindir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1-19
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1-18
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1-17
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1-16
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1-15
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1-14
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1-13
- Bump up version to compile with new go
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1-12
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1-11
- Bump up version to compile with new go
*   Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1-10
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1-9
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1-8
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1-7
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
