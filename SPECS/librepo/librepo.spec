#dont terminate build for unpackaged files.
%define _unpackaged_files_terminate_build 0

Summary:       	Repodata downloading library
Name:          	librepo
Version:       	1.17
Release:       	1
License:       	LGPLv2+
URL:           	https://github.com/Tojaj/librepo/
Group:         	System Environment/Libraries
Source0:       	%{name}-%{version}.tar.bz2
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	curl, gpgme, libassuan, libgpg-error
Requires:	expat
Requires:	glib
BuildRequires:	cmake
BuildRequires:	glib-devel
BuildRequires:	check
BuildRequires:	expat
BuildRequires:	curl
BuildRequires:	python2-devel
BuildRequires:	python2-libs
BuildRequires:	python2-tools
BuildRequires:	gpgme-devel
BuildRequires:	openssl-devel
BuildRequires:	attr
%description
A library providing C and Python (libcURL like) API for downloading 
linux repository metadata and packages

%prep
%setup -q

%build
mkdir build
cd build
cmake ..
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/librepo
cp %{_builddir}/%{name}-%{version}/build/librepo/librepo.so* %{buildroot}%{_libdir}
cp %{_builddir}/%{name}-%{version}/librepo/*.h %{buildroot}%{_includedir}/librepo

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/librepo.so*
%{_includedir}/librepo/*.h

%changelog
* Tue Dec 30 2014 Priyesh Padmavilasom <ppadmavilasom@vmware.com>
- initial specfile.

# EOF
