Summary:    The New GNU Portable Threads Library.
Name:       npth
Version:    1.6
Release:    2%{?dist}
URL:        https://github.com/gpg/npth
Group:      System Environment/Libraries.
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/gpg/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=408d99acfc4770d5f779802415b20ab14a6fb5e60cf5b368664913e80de6946419f8bbe483ecb04694e7d67a0320c5ac31e06eab3cfff5eb499356ac1ba77ced

Source1: license.txt
%include %{SOURCE1}

%description
This is a library to provide the GNU Pth API and thus a non-preemptive threads implementation.
In contrast to GNU Pth, it is based on the system's standard threads implementation.
This allows the use of libraries which are not compatible to GNU Pth.
Experience with a Windows Pth emulation showed that this is a solid way to provide
a co-routine based framework.

%package devel
Summary:       GNU npth development header and libraries.
Group:         Development/Libraries.
Requires:      npth = %{version}-%{release}

%description devel
Development package for npth.

%prep
%autosetup -n npth-%{name}-%{version}

%build
sh autogen.sh
%configure --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/aclocal/*

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.6-2
- Release bump for SRP compliance
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.6-1
- Upgrade to 1.6.
* Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> 1.3-1
- Initial Build.
