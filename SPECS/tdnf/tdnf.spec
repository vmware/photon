#
# tdnf spec file
#
Summary:	dnf/yum equivalent using C libs
Name:		tdnf
Version:	1.0.2
Release:	1%{?dist}
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
BuildRequires:	openssl-devel

BuildRequires:	librepo-devel
Source0:	%{name}-%{version}.tar.gz
%define sha1 tdnf=c17584cd75598ca951bb95099e3f76a975003b25

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
%setup -q

%build
autoreconf -i
./configure --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --sysconfdir=/etc
make %{?_smp_mflags}

%install
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
    %exclude %{_libdir}/debug

%changelog
*       Thu Jul 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2
-       Support reinstalls in transaction. Handle non-existent packages correctly.
*       Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.1-2
-       Create -debuginfo package. Use parallel make.
*       Tue Jun 30 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1
-       Proxy support, keepcache fix, valgrind leaks fix
*       Fri Jan 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0
-       Initial build.  First version

