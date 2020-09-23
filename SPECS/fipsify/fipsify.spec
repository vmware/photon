Summary:        fipsify - Enable fips, add fips module to initrd and generate hmac files.
Name:           fipsify
Version:        1.0
Release:        2%{?dist}
License:        GPLv2+
URL:            http://dl.bintray.com/vmware/photon_sources/1.0/fipsify-1.0.tar.gz
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        modules.fips
Source1:        fips.conf
Requires:	initramfs
Requires:	photon-checksum-generator

%description
Enable fips, add fips module to initrd and generate initrd.

%install
echo %{buildroot}
install -vdm 755 %{buildroot}/lib/modules/
cp %{SOURCE0} %{buildroot}/lib/modules/

mkdir -p %{buildroot}%{_sysconfdir}/dracut.conf.d
install -D -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/dracut.conf.d/

%postun

%post

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/dracut.conf.d/fips.conf
/lib/modules/modules.fips

%changelog
*   Wed Sep 23 2020 Michelle Wang <michellew@vmware.com> 1.0-2
-   Add sources fipsify-1.0.tar.gz to file OSSTP ticket
*   Tue Jan 28 2020 Vikash Bansal <bvikas@vmware.com> 1.0-1
-   Added fipsify package to photon-3.0
