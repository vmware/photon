#
# tdnf spec file
#

#dont terminate build for unpackaged files.
%define _unpackaged_files_terminate_build 0

Summary:	dnf/yum equivalent using C libs
Name:		tdnf
Version:	1.0
Release:	1
Vendor:		VMware, Inc.
Distribution:	Photon
License:	VMware
Url:		http://www.vmware.com
Group:		Applications/RPM
Requires:	hawkey, librepo, rpm
BuildRequires:	popt-devel
BuildRequires:	rpm-devel
BuildRequires:	glib-devel
BuildRequires:	hawkey-devel
BuildRequires:	librepo
Source0:	%{name}-%{version}.tar.gz

%description
tdnf is a yum/dnf equivalent
which uses libhawkey and librepo

%package	devel
Summary:	A Library providing C API for tdnf
Group:		Development/Libraries
Requires:	tdnf = %{version}-%{release}

%description devel
Development files for tdnf

%prep
rm -rf $RPM_BUILD_DIR/tdnf
zcat $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz | tar -xvf -

%build
cd $RPM_BUILD_DIR/tdnf
./configure --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --sysconfdir=/etc
make clean
make

%install
cd $RPM_BUILD_DIR/tdnf
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/var/cache/tdnf

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig
    ln -sf %{_bindir}/tdnf %{_bindir}/tyum

# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

# Post-uninstall
%postun

    /sbin/ldconfig
    rm -f %{_bindir}/tyum

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%files
    %defattr(-,root,root,0755)
    %{_bindir}/tdnf
    %{_libdir}/*.so*
    /etc/tdnf/*
    #/etc/yum.repos.d/*
    %dir /var/cache/tdnf

%files devel
    %defattr(-,root,root)
    %{_includedir}/*
    %{_libdir}/*

%changelog
*       Fri Jan 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0
-       Initial build.  First version

