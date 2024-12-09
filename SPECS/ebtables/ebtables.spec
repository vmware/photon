Summary:        A filtering tool for a Linux-based bridging firewall.
Name:           ebtables
Version:        2.0.11
Release:        3%{?dist}
URL:            http://ebtables.netfilter.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.netfilter.org/pub/ebtables/%{name}-%{version}.tar.gz
%define sha512  %{name}=43a04c6174c8028c501591ef260526297e0f018016f226e2a3bcf80766fddf53d4605c347554d6da7c4ab5e2131584a18da20916ffddcbf2d26ac93b00c5777f
Source1:        %{name}
Source2:        %{name}.service
Source3:        %{name}-config

Source4: license.txt
%include %{SOURCE4}

Patch0:         0001-ebtables-Initialise-len-and-flags-in-ebt_nflog_info-.patch

BuildRequires:  systemd-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  make

Requires:       systemd
Requires:       chkconfig

%description
Ethernet bridge tables is a firewalling tool to transparently filter network
traffic passing a bridge. The filtering possibilities are limited to link
layer filtering and some basic filtering on higher network layers.

This tool is the userspace control for the bridge and %{name} kernel
components (built by default in Fedora kernels).

The %{name} tool can be used together with the other Linux filtering tools,
like iptables. There are no known incompatibility issues.

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure --disable-silent-rules LOCKFILE=/run/%{name}.lock
%make_build

%install
%make_install

rm -f %{buildroot}%{_libdir}/*.la

mkdir -p %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_sysconfdir}/systemd/scripts
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/systemd/scripts/%{name}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 600 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/ebtables-config

# prepare for alternatives
touch %{buildroot}%{_sbindir}/%{name}{,-save,-restore}

install -vdm755 %{buildroot}%{_presetdir}
echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

%preun
%systemd_preun ebtables.service

%post
/sbin/ldconfig
alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-legacy 10000 \
  --slave %{_sbindir}/%{name}-save %{name}-save %{_sbindir}/%{name}-legacy-save \
  --slave %{_sbindir}/%{name}-restore %{name}-restore %{_sbindir}/%{name}-legacy-restore
%systemd_post ebtables.service

%postun
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]; then
  alternatives --remove %{name} %{_sbindir}/%{name}-legacy
fi
/sbin/ldconfig
%systemd_postun_with_restart ebtables.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_unitdir}/*
%{_presetdir}/50-%{name}.preset
%config(noreplace) %{_sysconfdir}/ethertypes
%{_sysconfdir}/systemd/scripts/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-config
%ghost %{_sbindir}/ebtables{,-save,-restore}

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.0.11-3
- Release bump for SRP compliance
* Sun Jan 22 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.0.11-2
- Use alternatives for ebtables
* Wed May 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.11-1
- Upgrade to v2.0.11
- Initialise len and flags in ebt_nflog_info structure
* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 2.0.10-4
- Commented out %check due to the limited chroot environment of bind.
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.10-3
- Disabled ebtables service by default
* Mon May 15 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.10-2
- Added systemd to Requires and BuildRequires.
* Wed Jan 18 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.10-1
- Initial build.
