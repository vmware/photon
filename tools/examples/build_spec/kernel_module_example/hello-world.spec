%define linux_esx_ver 5.10.152

Summary:        Hello World Linux module
Name:           hello-world
Version:        1.0
Release:        1%{?dist}
License:    	GPLv2
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        hello-world.tar.gz
BuildRequires:  linux-esx-devel = %{linux_esx_ver}
BuildRequires:  kmod
Requires:       linux-esx = %{linux_esx_ver}

%description
Example of building linux module for Photon OS

%prep
%autosetup -n hello-world

%build
make -C `echo /usr/src/linux-headers-%{linux_esx_ver}*` M=`pwd` VERBOSE=1 modules %{?_smp_mflags}

%install
make -C `echo /usr/src/linux-headers-%{linux_esx_ver}*` M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}
# fix permissins to generate non empty debuginfo
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%ldconfig_scriptlets

%post
/sbin/depmod -a

%files
%defattr(-,root,root)
/lib/modules/*

%changelog
*   Mon Oct 17 2022 User <user@example.org> 1.0-1
-   Initial build. First version
