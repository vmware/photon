Summary:	Photon release files
Name:		photon-release
Version:	1.0
Release:	3%{?dist}
License:	Apache License
Group:		System Environment/Base
URL:		https://vmware.github.io/photon/
Source:		%{name}-%{version}.2.tar.gz
%define sha1 photon-release=4c03ec658315e25873e5e5f3e77c0006ddfeecc6
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	photon-release
BuildArch:	noarch
Requires:       rpm

%description
Photon release files such as yum configs and other /etc/ release related files

%prep
%setup -q -n %{name}-%{version}.2

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT/usr/lib
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in *repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 VMWARE-RPM-GPG-KEY $RPM_BUILD_ROOT/etc/pki/rpm-gpg

echo "VMware Photon Linux %{photon_release_version}" > %{buildroot}/etc/photon-release
echo "PHOTON_BUILD_NUMBER=%{photon_build_number}" >> %{buildroot}/etc/photon-release

cat > %{buildroot}/etc/lsb-release <<- "EOF"
DISTRIB_ID="VMware Photon"
DISTRIB_RELEASE="%{photon_release_version}"
DISTRIB_CODENAME=Photon
DISTRIB_DESCRIPTION="VMware Photon %{photon_release_version}"
EOF

version_id=`echo %{photon_release_version} | grep -o -E '[0-9]+.[0-9]+'`
cat > %{buildroot}/usr/lib/os-release << EOF
NAME="VMware Photon"
VERSION="%{photon_release_version}"
ID=photon
VERSION_ID=$version_id
PRETTY_NAME="VMware Photon/Linux"
ANSI_COLOR="1;34"
HOME_URL="https://vmware.github.io/photon/"
BUG_REPORT_URL="https://github.com/vmware/photon/issues"
EOF

ln -sv ../usr/lib/os-release %{buildroot}/etc/os-release

cat > %{buildroot}/etc/issue <<- "EOF"
Welcome to Photon 1.0 (x86_64) - Kernel \r (\l)
EOF

cat > %{buildroot}/etc/issue.net <<- "EOF"
Welcome to Photon 1.0 (x86_64) - Kernel %r (%t)
EOF

%post
# Remove __db* files to workaround BD version check bug in rpm
rm -f /var/lib/rpm/__db*
rpm --import /etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
/etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
%config(noreplace) /etc/yum.repos.d/photon-iso.repo
%config(noreplace) /etc/yum.repos.d/photon.repo
%config(noreplace) /etc/yum.repos.d/photon-updates.repo
%config(noreplace) /etc/yum.repos.d/lightwave.repo
%config(noreplace) /etc/yum.repos.d/photon-extras.repo
%config(noreplace) /etc/photon-release
%config(noreplace) /etc/lsb-release
%config(noreplace) /usr/lib/os-release
%config(noreplace) /etc/os-release
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net

%changelog
*  		Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-3
-		yum repo gpgkey to VMWARE-RPM-GPG-KEY.
*  		Tue Mar 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0-2
-		Add revision to photon-release
*       Mon Jan 11 2016 Anish Swaminathan <anishs@vmware.com> 1.0-1
-       Reset version to match with Photon version
*       Mon Jan 04 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4
-       Adding photon-extras.repo
*	Thu Nov 19 2015 Anish Swaminathan <anishs@vmware.com> 1.3-1
-	Upgrade photon repo
*       Fri Aug 14 2015 Sharath George <sharathg@vmware.com> 1.2
-       Install photon repo links
*       Wed Jun 17 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1
-       Install photon key
