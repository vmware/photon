Summary:        Simple Linux module
Name:           simple-module
Version:        4.18.9
Release:        5%{?dist}
License:    	GPLv2
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        module_example.tar.xz
BuildRequires:  linux-devel = 4.18.9
BuildRequires:  kmod
Requires:       linux = 4.18.9

%description
Example of building linux module for Photon OS

%prep
%setup -q -n module_example

%build
make -C `echo /usr/src/linux-headers-4.18.9*` M=`pwd` VERBOSE=1 modules %{?_smp_mflags}

%install
make -C `echo /usr/src/linux-headers-4.18.9*` M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install
# fix permissins to generate non empty debuginfo
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%post
/sbin/depmod -a

%files
%defattr(-,root,root)
/lib/modules/*

%changelog
*   Tue Dec 04 2018 Alexey Makhalov <amakhalov@vmware.com> 4.18.9-5
-   Initial build. First version

