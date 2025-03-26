Summary:        A tool that inspect which pages of a file or files are being cached by the Linux kernel
Name:           pcstat
Version:        1
Release:        24%{?dist}
URL:            https://github.com/tobert/%{name}
Group:          Development/Debuggers
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/tobert/%{name}/archive/%{name}-1.zip
Source1:        https://github.com/golang/sys/golang-sys-08-02-2017.zip

Source2: license.txt
%include %{SOURCE2}
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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1-24
- Release bump for SRP compliance
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1-23
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1-22
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1-21
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 1-20
- Bump version as a part of go upgrade
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
