%global security_hardening none
Summary:	The Behavioral Activity Monitor With Container Support
Name:		falco
Version:	0.2.0
Release:	3%{?kernelsubrelease}%{?dist}
License:	GPLv2	  
URL:		http://www.sysdig.org/falco/
Group:		Applications/System	
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/draios/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 falco=c40840c6dcbd25fd1d0bf8aa2d1f77b1f5a7cde2
Source1:	https://github.com/draios/sysdig/archive/sysdig-0.10.1.tar.gz
%define sha1 sysdig=272b95ad02be4d194bba66d360ff935084d9c842
Source2:        http://stedolan.github.io/jq/download/linux64/jq
%define sha1 jq=e820e9e91c9cce6154f52949a3b2a451c4de8af4
Source3:        http://libvirt.org/sources/libvirt-2.0.0.tar.xz
%define sha1 libvirt=9a923b06df23f7a5526e4ec679cdadf4eb35a38f

BuildRequires:	cmake
BuildRequires:	openssl-devel
BuildRequires:	curl
BuildRequires:	zlib-devel
BuildRequires:	ncurses-devel
BuildRequires:  automake
BuildRequires:	linux-devel = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
BuildRequires:  autoconf 
BuildRequires:  libgcrypt 
BuildRequires:  sysdig
BuildRequires:  git
BuildRequires:  lua-devel
BuildRequires:  libyaml-devel
BuildRequires:  linux-api-headers
Requires:	zlib
Requires:	ncurses
Requires:	openssl
Requires:	curl
Requires:	libyaml
Requires:	lua
Requires:	sysdig

%description
Sysdig falco is an open source, behavioral activity monitor designed to detect anomalous activity in your applications. Falco lets you continuously monitor and detect container, application, host, and network activity... all in one place, from one source of data, with one set of customizable rules. 

%prep
%setup
%setup -T -D -a 1
chmod +x %{SOURCE2}
cp %{SOURCE2} /usr/bin
tar xf %{SOURCE3}

%build
mv sysdig-0.10.1 ../sysdig
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} CMakeLists.txt
make KERNELDIR="/lib/modules/%{KERNEL_VERSION}/build"

%install
make install KERNELDIR="/lib/modules/%{KERNEL_VERSION}/build" DESTDIR=%{buildroot}

%check
easy_install pip
pip install avocado-framework
pip install fabric
pip install aexpect
test/run_regression_tests.sh

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_usrsrc}/*
/etc/*
%{_datadir}/*

%changelog
*	Fri Sep  2 2016 Alexey Makhalov <amakhalov@vmware.com> 0.2.0-3
-	Use KERNEL_VERSION macro
*	Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.2.0-2
-	Removed packaging of debug files
*	Tue Jun 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.2.0-1
-	Initial build.	First version
