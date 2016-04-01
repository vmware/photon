#
# tdnf spec file
#
Summary:	dnf/yum equivalent using C libs
Name:		tdnf
Version:	1.0.8
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
%define sha1 tdnf=af0dcafda160822db158dc569e97e7655dcf50b2

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
    %config(noreplace) %{_sysconfdir}/tdnf/tdnf.conf
    %dir /var/cache/tdnf

%files devel
    %defattr(-,root,root)
    %{_includedir}/*
    %{_libdir}/*.a
    %{_libdir}/*.la
    %exclude %{_libdir}/debug

%changelog
*       Fri Apr 1 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8
-       Code scan fixes, autotest path fix, support --releasever
*       Thu Jan 14 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.7
-       Fix return codes on install and check-update
-       Add tests for install existing and update
*       Wed Jan 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.6
-       Support distroverpkg and add tests to work with make check
*       Mon Dec 14 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.5
-       Support for multiple packages in alter commands
-       Support url vars for releasever and basearch
*       Fri Oct 2 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.4
-       Fix upgrade to work without args, Engage distro-sync
-       Fix install to resolve to latest available
-       Fix formats, fix refresh on download output
*       Tue Sep 8 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.3
-       Fix metadata creation issues. Engage refresh flag.
-       Do not check gpgkey when gpgcheck is turned off in repo.
*       Thu Jul 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2
-       Support reinstalls in transaction. Handle non-existent packages correctly.
*       Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.1-2
-       Create -debuginfo package. Use parallel make.
*       Tue Jun 30 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1
-       Proxy support, keepcache fix, valgrind leaks fix
*       Fri Jan 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0
-       Initial build.  First version

