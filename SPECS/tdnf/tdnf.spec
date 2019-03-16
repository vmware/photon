#
# tdnf spec file
#
Summary:	dnf/yum equivalent using C libs
Name:		tdnf
Version:	1.1.0
Release:	4%{?dist}
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
%define sha1 tdnf=15544a87ea01d6215fed35bd2d1299776f7daca1
Patch0:         tdnf_print_curl_error.patch
Patch1:         tdnf-Installing-Updating-print.patch

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
%patch0 -p1
%patch1 -p1

%build
autoreconf -i
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/var/cache/tdnf
ln -sf %{_bindir}/tdnf %{buildroot}%{_bindir}/tyum

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig

# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

# Post-uninstall
%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%files
    %defattr(-,root,root,0755)
    %{_bindir}/tdnf
    %{_bindir}/tyum
    %{_libdir}/*.so*
    %config(noreplace) %{_sysconfdir}/tdnf/tdnf.conf
    %dir /var/cache/tdnf

%files devel
    %defattr(-,root,root)
    %{_includedir}/tdnf/*.h
    %{_libdir}/*.a
    %{_libdir}/*.la
    %exclude %{_libdir}/debug
    %{_libdir}/pkgconfig/tdnf.pc

%changelog
*       Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 1.1.0-4
-       fix package listing, add transaction progress
*       Wed Oct 11 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-3
-       Patch to report curl error for repo sync or download
*       Fri Sep 29 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-2
-       rpm version update
*       Thu Dec 08 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-1
-       update to v1.1.0
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.9-2
-	GA - Bump release of all rpms
*       Fri May 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.9-1
-       Update to 1.0.9. Contains fixes for updateinfo.
*       Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8-3
-       Fix link installs, fix devel header dir
*       Fri Apr 1 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8-2
-       Update version which was missed with 1.0.8-1, apply string limits
*       Fri Apr 1 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8-1
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

