Summary:        A tool that inspect which pages of a file or files are being cached by the Linux kernel
Name:           pcstat 
Version:        1
Release:        4%{?dist}
License:        Apache 
URL:            https://github.com/tobert/pcstat
Group:          Development/Debuggers
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/tobert/pcstat/archive/pcstat-1.zip
%define sha1    pcstat=cd67c42d291763597dbe3fb19e8e367c54a4a898
BuildRequires:  unzip go audit git
Requires:       go
%description
A tool that inspect which pages of a file or files are being cached by the Linux kernel

%prep
%setup -qn pcstat-master
%build
cd ..
mkdir -p build/src/github.com/tobert/pcstat
mkdir -p build/bin
cp -r pcstat-master/* build/src/github.com/tobert/pcstat/.
cd build
export GOPATH=`pwd`
cd bin
export GOBIN=`pwd`
export PATH=$PATH:$GOBIN
go get golang.org/x/sys/unix
cd ../src/github.com/tobert/pcstat
go build
cd pcstat
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
*   Tue Mar 07 2017 XIaolin Li <xiaolinl@vmware.com> 1-4
-   Moved executable from /usr/local/bin to /usr/bin.
*   Fri Feb 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1-3
-   Fix the build.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1-2
-   GA - Bump release of all rpms
*   Wed Nov 25 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.7.3-1
-   Initial build.  First version
