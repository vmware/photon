Summary:        Improved implementation of Network Time Protocol
Name:           ntpsec
Version:        1.2.3
Release:        2%{?dist}
Group:          System Environment/NetworkingPrograms
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://www.ntpsec.org/
Source0:        https://ftp.ntpsec.org/pub/releases/%{name}-%{version}.tar.gz
Source1:        %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}

Patch0:         ntpstats_path.patch

BuildRequires:  binutils
BuildRequires:  bison
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  libcap-devel
BuildRequires:  linux-api-headers
BuildRequires:  m4
BuildRequires:  openssl-devel
BuildRequires:  python3-attrs
BuildRequires:  python3-devel
BuildRequires:  systemd-devel

Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires:       gcc
Requires:       glibc
Requires:       openssl
Requires:       libevent
Requires:       libcap
Requires:       systemd

Conflicts:      ntp

%description
NTPsec is a more secure and improved implementation of the Network Time
Protocol derived from the original NTP project.

%package -n python3-ntp
Summary:        Python ntpsec bindings
Group:          Development/Languages/Python
Requires:       python3

%description -n python3-ntp
The ntpsec python bindings used by various ntp utilities.

%prep
%autosetup -p1 -n %{name}-NTPsec_1_2_3

%build
export CFLAGS="%{optflags}"
export CCFLAGS="%{optflags}"
python3 ./waf configure \
    --enable-debug \
    --prefix=%{_prefix} \
    --python=%{python3} \
    --pythonarchdir=%{python3_sitearch} \
    --libdir=%{_libdir}

python3 ./waf build --notests

%install
python3 ./waf --destdir=%{buildroot} install --notests

mkdir -p %{buildroot}/{%{_sysconfdir}/logrotate.d,%{_libdir}/systemd/ntp-units.d,\
%{_sharedstatedir}/ntp,%{_localstatedir}/log/ntpstats}
install -p -m755 attic/ntpdate %{buildroot}%{_sbindir}/ntpdate
install -p -m644 etc/logrotate-config.ntpd \
        %{buildroot}%{_sysconfdir}/logrotate.d/ntpsec.conf
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers
touch %{buildroot}%{_sharedstatedir}/ntp/ntp.drift
echo 'ntpd.service' > %{buildroot}%{_libdir}/systemd/ntp-units.d/60-ntpd.list

cat > %{buildroot}/etc/ntp.conf <<- "EOF"
tinker panic 0
restrict default kod nomodify notrap nopeer noquery
restrict 127.0.0.1
restrict -6 ::1
driftfile /var/lib/ntp/drift/ntp.drift
EOF

rm -rf %{buildroot}%{_docdir}

%check
python3 ./waf check --verbose %{?_smp_mflags}

%pre
%sysusers_create_compat %{SOURCE1}

%post
%{_sbindir}/ldconfig
%systemd_post ntpd.service ntp-wait.service

%preun
%systemd_preun ntpd.service ntp-wait.service

%postun
%{_sbindir}/ldconfig
%systemd_postun_with_restart ntpd.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/logrotate.d
%attr(0750, root, root) %config(noreplace) %{_sysconfdir}/ntp.conf
%attr(0750, root, root) %config(noreplace) %{_sysconfdir}/logrotate.d/ntpsec.conf
%attr(644,ntp,ntp) %{_sharedstatedir}/ntp/ntp.drift
%{_bindir}/ntp*
%{_sbindir}/ntp*
%{_unitdir}/ntp*.service
%{_unitdir}/ntp*.timer
%{_libdir}/libntpc.so*
%{_prefix}/lib/systemd/ntp-units.d/*ntpd.list
%dir %attr(-,ntp,ntp) %{_sharedstatedir}/ntp
%dir %attr(-,ntp,ntp) %{_localstatedir}/log/ntpstats
%{_sysusersdir}/%{name}.sysusers

%files -n python3-ntp
%defattr(-,root,root)
%{python3_sitearch}/ntp*

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.3-2
- Release bump for SRP compliance
* Mon Jan 22 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.2.3-1
- Update to 1.2.3, Fixes CVE-2023-4012
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.2.2-2
- Use systemd-rpm-macros for user creation
* Fri May 27 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.2.2-1
- ntpsec initial build
