Summary:        Usermode tools for VmWare virts
Name:           open-vm-tools
Version:        10.2.5
Release:        6%{?dist}
License:        LGPLv2+
URL:            https://github.com/vmware/open-vm-tools
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/vmware/open-vm-tools/archive/%{name}-stable-%{version}.tar.gz
%define sha1 open-vm-tools=f2eea3df2145bf898acd2f021bb1c745774d8222
Source1:        gosc-scripts-1.2.tar.gz
%define sha1 gosc-scripts-1.2=5031dd9b3b0569a40d2ee0caaa55a1cbf782345e
Source2:        vmtoolsd.service
Source3:        vgauthd.service
Patch0:         GOSC-libDeploy.patch
Patch1:         IPv6Support.patch
Patch2:         hostnameReCustomizationFix.patch
Patch3:         PureIPv6-hosts.patch
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet
BuildRequires:  libmspack
BuildRequires:  Linux-PAM
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  fuse-devel
BuildRequires:  systemd
Requires:       fuse
Requires:       xerces-c
Requires:       libdnet
Requires:       libmspack
Requires:       glib
Requires:       xml-security-c
Requires:       openssl
Requires:       systemd
%description
VmWare virtualization user mode tools
%prep
%setup -q -n %{name}-stable-%{version}/%{name}
%setup -a 1 -n %{name}-stable-%{version}/%{name}
%patch0 -p2
%patch1 -p0
%patch2 -p0
%patch3 -p0
%build
touch ChangeLog
autoreconf -i
sh ./configure --prefix=/usr --without-x --without-kernel-modules --without-icu --disable-static
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
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_bindir}/*
%{_sysconfdir}/*
%{_datadir}/*
/lib/*
%{_sbindir}/*


%changelog
*   Thu Feb 07 2019 Ankit Jain <ankitja@vmware.com> 10.2.5-1
-   Updating version to 10.2.5
*   Mon Apr 23 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 10.2.0-5
-   Bump release number to pick up changes to xerces-c.
*   Mon Apr 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 10.2.0-4
-   Revert regex changes to gosc scripts.
*   Wed Mar 14 2018 Anish Swaminathan <anishs@vmware.com> 10.2.0-3
-   Fix gosc patch to call customization
*   Wed Mar 14 2018 Anish Swaminathan <anishs@vmware.com> 10.2.0-2
-   Fix gosc scripts to take care of multiple network files per interface
*   Wed Jan 24 2018 Kumar Kaushik <kaushikk@vmware.com> 10.2.0-1
-   Updating to version 10.2.0
*   Thu Nov 30 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.5-3
-   Revert changing systemd service file dependency with cloud-init.
*   Fri Nov 17 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.5-2
-   Changing systemd service file dependency with cloud-init.
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
*       Fri Apr 29 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-8
-       Combining all GOSC scripts patches and fixing bug#1648133.
*       Tue Apr 19 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-7
-       Fixing libDeploy not to overwrite for SRM cust needs.
*       Tue Mar 29 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-6
-       Replacing timedatectl with systemd patch..
*       Fri Mar 25 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-5
-       Time data ctl fix for ignoring message print in stderr.
*       Tue Feb 09 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 10.0.5-4
-       Preserve network onboot config.
*       Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-3
-       Add vgauthd service.
*       Tue Feb 02 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-2
-       Making interface file name according to convention.
*       Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-1
-       Upgrade version.
*       Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 10.0.0-13
-       Edit post script.
*       Fri Nov 27 2015 Sharath George <sharathg@vmware.com> 10.0.0-12
-       Correcting path of pam file.
*       Tue Sep 15 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-11
-       Adding ssh RSA public support for password-less login.
*       Wed Sep 09 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-10
-       Adding option to modify /etc/hosts for lightwave on optional basis.
*       Wed Sep 09 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-9
-       Fixing once in while issue related to customization failure.
*       Wed Sep 02 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-8
-       Fixing systemd cloud-init and GOSC cloud-init race.
*       Tue Sep 01 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-7
-       Fixing GOSC counter bug.
*       Wed Aug 26 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-6
-       Avoiding reboot after successful customization.
*       Tue Aug 25 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-5
-       Adding support for NFS mount in GOSC scripts.
*       Thu Aug 20 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-4
-       Fixing GOSC-libdeploy return code problem.
*       Thu Aug 13 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-3
-       Combining all GOSC patches and adding support for lightwave.
*       Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-2
-       Build with fuse support.
*       Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-1
-       Update version to 10.0.0.
*       Tue Aug 11 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-7
-       VCA initial login password issue fix.
*       Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-6
-       Adding preun and post install commands.
*       Thu Jul 30 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-5
-       Adding Blob configuation support to GOSC scripts.
*       Thu Jul 09 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-4
-       Fixing GOSC to work on VCA.
*       Tue Apr 21 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-3
-       Adding guest optimizations support for photon.
*       Tue Apr 21 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.0-2
-       Added open-vm-tools-stderr_r-fix upstream patch and removed glibc patch.
*       Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 9.10.0-1
-       Initial version
