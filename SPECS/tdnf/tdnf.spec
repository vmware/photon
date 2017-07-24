#
# tdnf spec file
#
Summary:        dnf/yum equivalent using C libs
Name:           tdnf
Version:        1.2.1
Release:        2%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        LGPLv2.1,GPLv2
Url:            http://www.vmware.com
Group:          Applications/RPM
Requires:       hawkey >= 2017.1
Requires:       rpm-libs
Requires:       curl
BuildRequires:  popt-devel
BuildRequires:  rpm-devel
BuildRequires:  hawkey-devel >= 2017.1
BuildRequires:  openssl-devel
BuildRequires:  libsolv-devel
BuildRequires:  curl-devel
Source0:    %{name}-%{version}.tar.gz
Patch0:     tdnf_quiet_repo_refresh.patch
%define sha1 tdnf=ebbed639c68316e5a152b0bd277c1b040ee6871f
Source1:    cache-updateinfo
Source2:    cache-updateinfo.service
Source3:    cache-updateinfo.timer
Source4:    updateinfo.sh

%description
tdnf is a yum/dnf equivalent
which uses libhawkey and librepo

%package    devel
Summary:    A Library providing C API for tdnf
Group:      Development/Libraries
Requires:   tdnf = %{version}-%{release}
Requires:   hawkey-devel >= 2017.1

%description devel
Development files for tdnf

%package	cli-libs
Summary:	Library providing cli libs for tdnf like clients
Group:		Development/Libraries

%description cli-libs
Library providing cli libs for tdnf like clients.

%prep
%setup -q
%patch0 -p1


%build
sed -i 's/tdnf, 1.2.0/tdnf, 1.2.1/' configure.ac
autoreconf -i
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc   \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
mkdir -p %{buildroot}/var/cache/tdnf
ln -sf %{_bindir}/tdnf %{buildroot}%{_bindir}/tyum
install -v -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/tdnf-cache-updateinfo
install -v -D -m 0644 %{SOURCE2} %{buildroot}%{_libdir}/systemd/system/tdnf-cache-updateinfo.service
install -v -D -m 0644 %{SOURCE3} %{buildroot}%{_libdir}/systemd/system/tdnf-cache-updateinfo.timer
install -v -D -m 0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/motdgen.d/02-tdnf-updateinfo.sh

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig

%triggerin -- motd
[ $2 -eq 1 ] || exit 0
if [ $1 -eq 1 ]; then
    echo "detected install of tdnf/motd, enabling tdnf-cache-updateinfo.timer" >&2
    systemctl enable tdnf-cache-updateinfo.timer >/dev/null 2>&1 || :
    systemctl start tdnf-cache-updateinfo.timer >/dev/null 2>&1 || :
elif [ $1 -eq 2 ]; then
    echo "detected upgrade of tdnf, daemon-reload" >&2
    systemctl daemon-reload >/dev/null 2>&1 || :
fi


# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%triggerun -- motd
[ $1 -eq 1 ] && [ $2 -eq 1 ] && exit 0
echo "detected uninstall of tdnf/motd, disabling tdnf-cache-updateinfo.timer" >&2
systemctl --no-reload disable tdnf-cache-updateinfo.timer >/dev/null 2>&1 || :
systemctl stop tdnf-cache-updateinfo.timer >/dev/null 2>&1 || :
rm -rf /var/cache/tdnf/cached-updateinfo.txt

# Post-uninstall
%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%triggerpostun -- motd
[ $1 -eq 1 ] && [ $2 -eq 1 ] || exit 0
echo "detected upgrade of tdnf/motd, restarting tdnf-cache-updateinfo.timer" >&2
systemctl try-restart tdnf-cache-updateinfo.timer >/dev/null 2>&1 || :

%files
    %defattr(-,root,root,0755)
    %{_bindir}/tdnf
    %{_bindir}/tyum
    %{_bindir}/tdnf-cache-updateinfo
    %{_libdir}/*.so.*
    %config(noreplace) %{_sysconfdir}/tdnf/tdnf.conf
    %config %{_libdir}/systemd/system/tdnf-cache-updateinfo.service
    %config(noreplace) %{_libdir}/systemd/system/tdnf-cache-updateinfo.timer
    %config %{_sysconfdir}/motdgen.d/02-tdnf-updateinfo.sh
    %dir /var/cache/tdnf

%files devel
    %defattr(-,root,root)
    %{_includedir}/tdnf/*.h
    %{_libdir}/*.so
    %exclude %{_libdir}/debug
    %{_libdir}/pkgconfig/tdnf.pc
    %{_libdir}/pkgconfig/tdnf-cli-libs.pc

%files cli-libs
    %defattr(-,root,root)
    %{_libdir}/libtdnfcli.so.*

%changelog
*   Fri Jul 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-2
-   Modify quiet patch.
*   Tue Jul 18 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-1
-   Update to v1.2.1
*   Tue May 30 2017 Bo Gan <ganb@vmware.com> 1.2.0-5
-   Fix cache-updateinfo script again
*   Fri May 12 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-4
-   Patch repo refresh to allow quiet flags
*   Wed May 10 2017 Bo Gan <ganb@vmware.com> 1.2.0-3
-   Fix cache-updateinfo script
*   Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-2
-   Fix Requires for cli-libs
*   Wed May 03 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-   update to v1.2.0
*   Sun Apr 30 2017 Bo Gan <ganb@vmware.com> 1.1.0-5
-   Do not write to stdout in motd triggers
*   Thu Apr 20 2017 Bo Gan <ganb@vmware.com> 1.1.0-4
-   motd hooks/triggers for updateinfo notification
*   Fri Apr 14 2017 Dheerajs Shetty <dheerajs@vmware.com> 1.1.0-3
-   Adding a patch to compile with latest hawkey version
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.0-2
-   BuildRequires libsolv-devel.
*   Thu Dec 08 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-1
-   update to v1.1.0
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0.9-3
-   Use rpm-libs at runtime
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.9-2
-   GA - Bump release of all rpms
*   Fri May 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.9-1
-   Update to 1.0.9. Contains fixes for updateinfo.
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8-3
-   Fix link installs, fix devel header dir
*   Fri Apr 1 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8-2
-   Update version which was missed with 1.0.8-1, apply string limits
*   Fri Apr 1 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.8-1
-   Code scan fixes, autotest path fix, support --releasever
*   Thu Jan 14 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.7
-   Fix return codes on install and check-update
-   Add tests for install existing and update
*   Wed Jan 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.6
-   Support distroverpkg and add tests to work with make check
*   Mon Dec 14 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.5
-   Support for multiple packages in alter commands
-   Support url vars for releasever and basearch
*   Fri Oct 2 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.4
-   Fix upgrade to work without args, Engage distro-sync
-   Fix install to resolve to latest available
-   Fix formats, fix refresh on download output
*   Tue Sep 8 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.3
-   Fix metadata creation issues. Engage refresh flag.
-   Do not check gpgkey when gpgcheck is turned off in repo.
*   Thu Jul 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2
-   Support reinstalls in transaction. Handle non-existent packages correctly.
*   Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.1-2
-   Create -debuginfo package. Use parallel make.
*   Tue Jun 30 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1
-   Proxy support, keepcache fix, valgrind leaks fix
*   Fri Jan 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0
-   Initial build.  First version

