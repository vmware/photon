Name:           WALinuxAgent
Summary:        The Windows Azure Linux Agent
Version:        2.0.14
Release:        2%{?dist}
License:        Apache License Version 2.0
Group:          System/Daemons
Url:            http://go.microsoft.com/fwlink/?LinkId=250998
Source0:        %{name}-%{version}.tar.gz
Patch0:         photondistroadd.patch
%define sha1 WALinuxAgent=90448cc3f48f21a23a0932d1cf05e75d5a5bf158

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
Requires:       python-pyasn1
Requires:       openssh
Requires:       openssl
Requires:       util-linux
Requires:       sed
Requires:       grep
Requires:       sudo
Requires:       iptables

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Vendor:         Microsoft Corporation

%description
The Windows Azure Linux Agent supports the provisioning and running of Linux
VMs in the Windows Azure cloud. This package should be installed on Linux disk
images that are built to run in the Windows Azure environment.

%prep
%setup -q
find . -type f -exec sed -i 's/\r//' {} +
find . -type f -exec chmod 0644 {} +
%patch -P 0 -p1

%pre -p /bin/sh

%build
#%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --lnx-distro='photon' --init-system='systemd' --root=%{buildroot}
mkdir -p  %{buildroot}/%{_localstatedir}/log
mkdir -p -m 0700 %{buildroot}/%{_sharedstatedir}/waagent
touch %{buildroot}/%{_localstatedir}/log/waagent.log

%post
/sbin/chkconfig --add waagent

%preun -p /bin/sh
if [ $1 = 0 ]; then
	/sbin/service waagent stop >/dev/null 2>&1
	/sbin/chkconfig --del waagent
fi

%postun -p /bin/sh
if [ "$1" -ge "1" ]; then
	/sbin/service waagent restart >/dev/null 2>&1 || :
fi


%files
/usr/lib/systemd/system/*
#%attr(0755,root,root) %{_initddir}/waagent
%attr(0755,root,root) %{_sysconfdir}/udev/rules.d/99-azure-product-uuid.rules
%defattr(0644,root,root,0755)
%doc Changelog LICENSE-2.0.txt NOTICE README
%attr(0755,root,root) %{_sbindir}/waagent
%config(noreplace) %{_sysconfdir}/logrotate.d/waagent
%config %{_sysconfdir}/waagent.conf
%ghost %{_localstatedir}/log/waagent.log
%dir %attr(0700, root, root) %{_sharedstatedir}/waagent


%changelog
* Thu Aug 6 2015 Anish Swaminathan <anishs@vmware.com>
- Added sha1sum
* Fri Mar 13 2015 - mbassiouny@vmware.com
- Initial pacaking for Discus
