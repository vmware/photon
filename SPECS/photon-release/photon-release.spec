Summary:    Photon release files
Name:       photon-release
Version:    3.0
Release:    2%{?dist}
License:    Apache License
Group:      System Environment/Base
URL:        https://vmware.github.io/photon/
Vendor:     VMware, Inc.
Distribution:   Photon
BuildArch:  noarch

%description
Photon release files such as yum configs and other /etc/ release related files

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT/usr/lib

echo "VMware Photon OS %{photon_release_version}" > %{buildroot}/etc/photon-release
echo "PHOTON_BUILD_NUMBER=%{photon_build_number}" >> %{buildroot}/etc/photon-release

cat > %{buildroot}/etc/lsb-release <<- "EOF"
DISTRIB_ID="VMware Photon OS"
DISTRIB_RELEASE="%{photon_release_version}"
DISTRIB_CODENAME=Photon
DISTRIB_DESCRIPTION="VMware Photon OS %{photon_release_version}"
EOF

version_id=`echo %{photon_release_version} | grep -o -E '[0-9]+.[0-9]+'`
cat > %{buildroot}/usr/lib/os-release << EOF
NAME="VMware Photon OS"
VERSION="%{photon_release_version}"
ID=photon
VERSION_ID=$version_id
PRETTY_NAME="VMware Photon OS/Linux"
ANSI_COLOR="1;34"
HOME_URL="https://vmware.github.io/photon/"
BUG_REPORT_URL="https://github.com/vmware/photon/issues"
EOF

ln -sv ../usr/lib/os-release %{buildroot}/etc/os-release

cat > %{buildroot}/etc/issue <<- EOF
Welcome to Photon %{photon_release_version} (%{_arch}) - Kernel \r (\l)
EOF

cat > %{buildroot}/etc/issue.net <<- EOF
Welcome to Photon %{photon_release_version} (%{_arch}) - Kernel %r (%t)
EOF

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/photon-release
%config(noreplace) /etc/lsb-release
%config(noreplace) /usr/lib/os-release
%config(noreplace) /etc/os-release
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net

%changelog
*       Fri Sep 28 2018 Ajay Kaher <akaher@vmware.com> 3.0-2
-       Fix for aarch64
*       Mon Sep 24 2018 Anish Swaminathan <anishs@vmware.com> 3.0-1
-       Update to 3.0
*       Thu Jul 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0-1
-       update to 2.0
*       Wed Nov 30 2016 Anish Swaminathan <anishs@vmware.com> 1.0-7
-       Upgrade photon repo
*       Fri Nov 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-6
-       Remove requires for rpm
*       Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-5
-       GA - Bump release of all rpms
*       Mon Apr 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-4
-       Split up repo and gpg key files to photon-repos
*       Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-3
-       yum repo gpgkey to VMWARE-RPM-GPG-KEY.
*       Wed Mar 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-2
-       Add revision to photon-release
*       Mon Jan 11 2016 Anish Swaminathan <anishs@vmware.com> 1.0-1
-       Reset version to match with Photon version
*       Mon Jan 04 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4
-       Adding photon-extras.repo
*       Thu Nov 19 2015 Anish Swaminathan <anishs@vmware.com> 1.3-1
-       Upgrade photon repo
*       Fri Aug 14 2015 Sharath George <sharathg@vmware.com> 1.2
-       Install photon repo links
*       Wed Jun 17 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1
-       Install photon key
