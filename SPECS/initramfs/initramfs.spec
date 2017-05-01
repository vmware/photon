Summary:	initramfs
Name:		initramfs
Version:	2.0
Release:	1%{?dist}
Source0:	systemd.conf
Source1:	fscks.conf
License:	Apache License
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	initramfs
Requires:	dracut

%description
This package provides the configuration files for initrd generation.

%install
mkdir -p %{buildroot}%{_sysconfdir}/dracut.conf.d
install -D -m644 %{SOURCE0} %{buildroot}%{_sysconfdir}/dracut.conf.d/
install -D -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/dracut.conf.d/
install -d -m755 %{buildroot}%{_localstatedir}/lib/initramfs/kernel

%define watched_path %{_sbindir} %{_libdir}/udev/rules.d %{_libdir}/systemd/system  /lib/modules
%define watched_pkgs e2fsprogs, ostree, systemd, kpartx, device-mapper-multipath

%define removal_action \
rm -rf %{_localstatedir}/lib/rpm-state/initramfs.regenerate \
rm -rf %{_localstatedir}/lib/rpm-state/initramfs.pending

%define pkgs_trigger_action \
[ -f %{_localstatedir}/lib/rpm-state/initramfs.regenerate ] && exit 0 \
mkdir -p %{_localstatedir}/lib/rpm-state \
touch %{_localstatedir}/lib/rpm-state/initramfs.regenerate \
echo "initramfs (re)generation triggered"

%define file_trigger_action \
if [ -f %{_localstatedir}/lib/rpm-state/initramfs.regenerate ]; then \
    echo "(re)generate initramfs for all kernels" \
    mkinitrd -q \
elif [ -d %{_localstatedir}/lib/rpm-state/initramfs.pending ]; then \
    for k in `ls %{_localstatedir}/lib/rpm-state/initramfs.pending/`; do \
        echo "generate initramfs for $k" \
        mkinitrd -q /boot/initrd.img-$k $k \
    done; \
fi \
%{removal_action}

%post
%{pkgs_trigger_action}

%postun
[ $1 -eq 0 ] || exit 0
%{removal_action}

%posttrans
%{file_trigger_action}

%triggerin -- %{watched_pkgs}
%{pkgs_trigger_action}

%triggerun -- %{watched_pkgs}
%{pkgs_trigger_action}

%transfiletriggerin -- %{watched_path}
%{file_trigger_action}

%transfiletriggerpostun -- %{watched_path}
%{file_trigger_action}

%files
%defattr(-,root,root,-)
%{_sysconfdir}/dracut.conf.d/systemd.conf
%{_sysconfdir}/dracut.conf.d/fscks.conf
%dir %{_localstatedir}/lib/initramfs/kernel

%changelog
*   Wed Apr 12 2017 Bo Gan <ganb@vmware.com> 2.0-1
-   Made initrd generation dynamic, triggers for systemd, e2fs-progs
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-7
-   Expand uname -r to have release number
*   Wed Nov 23 2016 Anish Swaminathan <anishs@vmware.com>  1.0-6
-   Dracut module change to include systemd initrd target
*   Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-5
-   Added fsck tools
-   Use kernel version and release number in initrd file name
*   Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-4
-   Added kernel macros
*   Thu Jun 30 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-4
-   Exapand setup macro and remove the source file.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-3
-   GA - Bump release of all rpms
*   Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-2
-   Update to linux-4.4.8
*   Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-1
-   Initial version.
