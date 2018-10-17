Summary:        Usermode tools for VmWare virts
Name:           open-vm-tools
Version:        10.3.0
Release:        2%{?dist}
License:        LGPLv2+
URL:            https://github.com/vmware/open-vm-tools
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/vmware/open-vm-tools/archive/%{name}-%{version}-8931395.tar.gz
%define sha1 open-vm-tools=236d8159882ab2663043232a59f84eba144d0345
Source1:        gosc-scripts-1.2.tar.gz
%define sha1 gosc-scripts-1.2=5031dd9b3b0569a40d2ee0caaa55a1cbf782345e
Source2:        vmtoolsd.service
Source3:        vgauthd.service
Patch0:         IPv6Support.patch
Patch1:         hostnameReCustomizationFix.patch
Patch2:         PureIPv6-hosts.patch
Patch3:         GOSC-libDeploy.patch
Patch4:         timezoneCust.patch
Patch5:         gosc-post-custom.patch
BuildArch:      x86_64
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  fuse-devel
BuildRequires:  systemd
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  libtirpc-devel
BuildRequires:  xmlsec1-devel
Requires:       fuse
Requires:       xerces-c
Requires:       libdnet
Requires:       libmspack
Requires:       glib
Requires:       xml-security-c
Requires:       openssl
Requires:       systemd
Requires:       libstdc++
Requires:       libtirpc
Requires:       xmlsec1
%description
VmWare virtualization user mode tools

%package        devel
Summary:        Header and development files for open-vm-tools
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q -n %{name}-%{version}-8931395
%setup -a 1 -n %{name}-%{version}-8931395
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p2
%patch4 -p0
%patch5 -p0
%build
touch ChangeLog
autoreconf -i
sh ./configure --prefix=/usr --without-x --without-kernel-modules --without-icu --disable-static --with-tirpc
make %{?_smp_mflags}
%install

#collecting hacks to manually drop the vmhgfs module
install -vdm 755 %{buildroot}/lib/systemd/system
install -vdm 755 %{buildroot}/usr/share/open-vm-tools/GOSC/
cp -r gosc-scripts %{buildroot}/usr/share/open-vm-tools/GOSC
install -p -m 644 %{SOURCE2} %{buildroot}/lib/systemd/system
install -p -m 644 %{SOURCE3} %{buildroot}/lib/systemd/system

make DESTDIR=%{buildroot} install
rm -f %{buildroot}/sbin/mount.vmhgfs
chmod -x %{buildroot}/etc/pam.d/vmtoolsd
# Move vm-support to /usr/bin
mv %{buildroot}%{_sysconfdir}/vmware-tools/vm-support %{buildroot}%{_bindir}
find %{buildroot}/usr/lib/ -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post vgauthd.service vmtoolsd.service

%preun
%systemd_preun vmtoolsd.service vgauthd.service
# Tell VMware that open-vm-tools is being uninstalled
if [ "$1" = "0" -a                      \
     -e %{_bindir}/vmware-checkvm -a    \
     -e %{_bindir}/vmware-rpctool ] &&  \
     %{_bindir}/vmware-checkvm &> /dev/null; then
   %{_bindir}/vmware-rpctool 'tools.set.version 0' &> /dev/null || /bin/true
fi

%postun 
/sbin/ldconfig
%systemd_postun_with_restart vmtoolsd.service vgauthd.service

%files 
%defattr(-,root,root)
%{_libdir}/open-vm-tools/plugins/*
%{_libdir}/*.so.*
%{_bindir}/*
%{_sysconfdir}/*
%{_datadir}/*
/lib/*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so

%changelog
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 10.3.0-2
-   Adding BuildArch
*   Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 10.3.0-1
-   Version update. Use rpcsvc-proto, libtirpc, xmlsec1
*   Tue Jul 10 2018 Keerthana K <keerthanak@vmware.com> 10.2.0-4
-   Fix for post custom script failure.
*   Mon Apr 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 10.2.0-3
-   Revert regex changes to gosc scripts.
*   Wed Mar 21 2018 Anish Swaminathan <anishs@vmware.com> 10.2.0-2
-   Fix gosc patch to call customization
*   Wed Jan 24 2018 Kumar Kaushik <kaushikk@vmware.com> 10.2.0-1
-   Updating version to 10.2.0.
*   Tue Aug 22 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.10-1
-   Updating version to 10.1.10, removing upstream patches.
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 10.1.5-6
-   Add libdnet-devel and libmspack-devel to BuildRequires, add devel package.
*   Mon Jun 05 2017 Bo Gan <ganb@vmware.com> 10.1.5-5
-   Fix dependency
*   Thu Apr 20 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.5-4
-   Timezone customization, PR # 1684889
*   Fri Apr 07 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.5-3
-   Applying tmp race condition patch, PR #1733669
*   Fri Mar 24 2017 Alexey Makhalov <amakhalov@vmware.com> 10.1.5-2
-   Added *-sysmacros.patch to fix build issue with glibc-2.25
*   Fri Mar 03 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.5-1
-   Updating version to 10.1.5
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 10.1.0-2
-   BuildRequires Linux-PAM-devel
*   Mon Nov 21 2016 Kumar Kaushik <kaushikk@vmware.com> 10.1.0-1
-   Updating version to 10.1.0
*   Wed Oct 05 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-14
-   Adding proper entry to /etc/hosts for IPv6.
*   Tue Oct 04 2016 ChangLee <changLee@vmware.com> 10.0.5-13
-   Modified %check
*   Thu Jun 23 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-12
-   Avoiding recustomization of hostname, bug#1678537.
*   Mon Jun 13 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-11
-   Adding IPv6 Support for VCHA in customization.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 10.0.5-10
-   GA - Bump release of all rpms
*   Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-9
-   Edit scriptlets.
*   Fri Apr 29 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-8
-   Combining all GOSC scripts patches and fixing bug#1648133.
*   Tue Apr 19 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-7
-   Fixing libDeploy not to overwrite for SRM cust needs.
*   Tue Mar 29 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-6
-   Replacing timedatectl with systemd patch..
*   Fri Mar 25 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-5
-   Time data ctl fix for ignoring message print in stderr.
*   Tue Feb 09 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 10.0.5-4
-   Preserve network onboot config.
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-3
-   Add vgauthd service.
*   Tue Feb 02 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-2
-   Making interface file name according to convention.
*   Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-1
-   Upgrade version.
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 10.0.0-13
-   Edit post script.
*   Fri Nov 27 2015 Sharath George <sharathg@vmware.com> 10.0.0-12
-   Correcting path of pam file.
*   Tue Sep 15 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-11
-   Adding ssh RSA public support for password-less login.
*   Wed Sep 09 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-10
-   Adding option to modify /etc/hosts for lightwave on optional basis.
*   Wed Sep 09 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-9
-   Fixing once in while issue related to customization failure.
*   Wed Sep 02 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-8
-   Fixing systemd cloud-init and GOSC cloud-init race.
*   Tue Sep 01 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-7
-   Fixing GOSC counter bug.
*   Wed Aug 26 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-6
-   Avoiding reboot after successful customization.
*   Tue Aug 25 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-5
-   Adding support for NFS mount in GOSC scripts.
*   Thu Aug 20 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-4
-   Fixing GOSC-libdeploy return code problem.
*   Thu Aug 13 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-3
-   Combining all GOSC patches and adding support for lightwave.
*   Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-2
-   Build with fuse support.
*   Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-1
-   Update version to 10.0.0.
*   Tue Aug 11 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-7
-   VCA initial login password issue fix.
*   Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-6
-   Adding preun and post install commands.
*   Thu Jul 30 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-5
-   Adding Blob configuation support to GOSC scripts.
*   Thu Jul 09 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-4
-   Fixing GOSC to work on VCA.
*   Tue Apr 21 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-3
-   Adding guest optimizations support for photon.
*   Tue Apr 21 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.0-2
-   Added open-vm-tools-stderr_r-fix upstream patch and removed glibc patch.
*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 9.10.0-1
-   Initial version
