Summary:	Linux API header files
Name:		linux-api-headers
Version:	3.19.2
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://www.kernel.org/pub/linux/kernel/v3.x/linux-%{version}.tar.xz
%define sha1 linux=10a25ca5b6d93db78adc9caf13f7ad7cb4b79c61
BuildArch:	noarch
%description
The Linux API Headers expose the kernel's API for use by Glibc.
%prep
%setup -q -n linux-%{version}
%build
make mrproper
make headers_check
%install
cd %{_builddir}/linux-%{version}
make INSTALL_HDR_PATH=%{buildroot}%{_prefix} headers_install
find /%{buildroot}%{_includedir} \( -name .install -o -name ..install.cmd \) -delete
%files
%defattr(-,root,root)
%{_includedir}/*
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-	Initial build. First version
