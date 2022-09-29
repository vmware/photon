Summary:         RPC program number mapper
Name:            rpcbind
Version:         1.2.6
Release:         3%{?dist}
License:         BSD
URL:             http://nfsv4.bullopensource.org
Group:           Applications/Daemons
Vendor:          VMware, Inc.
Distribution:    Photon

Source0: http://downloads.sourceforge.net/rpcbind/%{name}-%{version}.tar.bz2
%define sha512 %{name}=fb89c61be4c533fe2e6057749d97079a2d1c9fac0d35d6be1a159a0edbf86092b3fc121f19fa920e75aac5ecdd3f59f5978e6401d5cad16cd438c977736206a7

Source1:         %{name}.service
Source2:         %{name}.socket
Source3:         %{name}.sysconfig

BuildRequires:   libtirpc-devel
BuildRequires:   systemd-devel

Requires:        libtirpc
Requires:        systemd
Requires(pre):   /usr/sbin/useradd /usr/sbin/userdel /usr/sbin/groupadd /usr/sbin/groupdel /usr/bin/false
Requires(preun): /usr/sbin/userdel /usr/sbin/groupdel
Requires(post):  /usr/bin/chown

%description
The rpcbind program is a replacement for portmap.
It is required for import or export of Network File System (NFS) shared directories.
The rpcbind utility is a server that converts RPC program numbers into universal addresses.

%prep
%autosetup -p1

%build
sed -i "/servname/s:%{name}:sunrpc:" src/%{name}.c
%configure \
            --enable-warmstarts \
            --disable-debug \
            --with-statedir=%{_sharedstatedir}/%{name} \
            --with-rpcuser=rpc

%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_sharedstatedir}/%{name} \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_sysconfdir}/sysconfig

install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -vdm755 %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/50-%{name}.preset << EOF
disable %{name}.socket
disable %{name}.service
EOF

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%pre
getent group rpc >/dev/null || groupadd -f -g 31 -r rpc
if ! getent passwd rpc >/dev/null ; then
  if ! getent passwd 31 >/dev/null ; then
    useradd -d %{_sharedstatedir}/%{name} -g rpc -s /bin/false -u 31 rpc > /dev/null 2>&1
  else
    useradd -d %{_sharedstatedir}/%{name} -g rpc -s /bin/false rpc > /dev/null 2>&1
  fi
fi

%preun
%systemd_preun %{name}.service %{name}.socket
if [ $1 -eq 0 ]; then
  userdel  rpc 2>/dev/null || :
  groupdel rpc 2>/dev/null || :
fi

%post
/sbin/ldconfig
if [ $1 -eq 1 ]; then
  chown -v root:sys %{_sharedstatedir}/%{name}
fi
%systemd_post %{name}.socket %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service %{name}.socket

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/*
%dir %{_localstatedir}/lib/%{name}
%{_unitdir}/*
%{_presetdir}/50-%{name}.preset

%changelog
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.6-3
- Bump version as a part of libtirpc upgrade
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.6-2
- Fix binary path
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.6-1
- Automatic Version Bump
* Fri Sep 21 2018 Keerthana K <keerthanak@vmware.com> 1.2.5-1
- Update to version 1.2.5
* Tue Mar 06 2018 Xiaolin Li <xiaolinl@vmware.com> 0.2.4-5
- Fix pre install script.
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 0.2.4-4
- Remove coreutils from requires and use explicit tools for post actions
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  0.2.4-3
- Disabled rpcbind service by default
* Thu May 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.4-2
- Fix CVE-2017-8779
* Wed Apr 5 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.2.4-1
- Updating to latest version
* Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.2.3-9
- add shadow and coreutils to requires
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  0.2.3-8
- Change systemd dependency
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.2.3-7
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.2.3-6
- GA - Bump release of all rpms
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 0.2.3-5
- Edit scriptlets.
* Fri Feb 05 2016 Anish Swaminathan <anishs@vmware.com> 0.2.3-4
- Add pre install scripts in the rpm
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 0.2.3-3
- Edit scripts in the rpm
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  0.2.3-2
- Add systemd to Requires and BuildRequires.
* Tue Dec 8 2015 Divya Thaluru <dthaluru@vmware.com> 0.2.3-1
- Initial build.  First version
